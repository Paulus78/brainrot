#!/usr/bin/env python3
"""Compare two spoken regions in a voice master without changing the audio."""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import shutil
import subprocess

import numpy as np


def find_ffmpeg() -> str:
    candidates = [
        os.environ.get("FFMPEG"),
        shutil.which("ffmpeg"),
        "/Applications/Streamlabs OBS.app/Contents/Resources/node_modules/ffmpeg-ffprobe-static/ffmpeg",
        "/Applications/VideoProc.app/Contents/Resources/transcoder.bundle/Contents/Resources/ffmpeg",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return candidate
    raise SystemExit("ffmpeg was not found")


def read_mono_f32(path: Path, sample_rate: int) -> np.ndarray:
    command = [
        find_ffmpeg(),
        "-loglevel",
        "error",
        "-i",
        str(path),
        "-vn",
        "-ac",
        "1",
        "-ar",
        str(sample_rate),
        "-f",
        "f32le",
        "-",
    ]
    data = subprocess.run(command, check=True, stdout=subprocess.PIPE).stdout
    return np.frombuffer(data, dtype="<f4").astype(np.float64)


def estimate_pitch(segment: np.ndarray, sample_rate: int) -> np.ndarray:
    frame_size = int(round(0.050 * sample_rate))
    hop = int(round(0.010 * sample_rate))
    min_lag = int(sample_rate / 350.0)
    max_lag = int(sample_rate / 70.0)
    window = np.hanning(frame_size)
    frame_rms: list[float] = []
    frames: list[np.ndarray] = []

    for start in range(0, max(0, len(segment) - frame_size + 1), hop):
        frame = segment[start : start + frame_size]
        rms = float(np.sqrt(np.mean(frame * frame)))
        frame_rms.append(rms)
        frames.append(frame)

    if not frames:
        return np.array([], dtype=np.float64)

    rms_gate = max(0.003, float(np.percentile(frame_rms, 35)) * 1.15)
    pitches: list[float] = []
    for frame, rms in zip(frames, frame_rms):
        if rms < rms_gate:
            continue
        centered = (frame - np.mean(frame)) * window
        spectrum = np.fft.rfft(centered, n=2 * frame_size)
        autocorr = np.fft.irfft(spectrum * np.conj(spectrum))[:frame_size]
        if autocorr[0] <= 0:
            continue
        search = autocorr[min_lag : max_lag + 1]
        lag = int(np.argmax(search)) + min_lag
        confidence = float(autocorr[lag] / autocorr[0])
        if confidence < 0.30:
            continue
        if 1 <= lag < len(autocorr) - 1:
            left, center, right = autocorr[lag - 1], autocorr[lag], autocorr[lag + 1]
            denominator = left - 2 * center + right
            if abs(denominator) > 1e-12:
                lag += 0.5 * (left - right) / denominator
        pitches.append(sample_rate / lag)
    return np.asarray(pitches, dtype=np.float64)


def analyze_region(audio: np.ndarray, sample_rate: int, start: float, end: float) -> dict[str, float | int]:
    segment = audio[int(start * sample_rate) : int(end * sample_rate)]
    pitches = estimate_pitch(segment, sample_rate)
    rms = float(np.sqrt(np.mean(segment * segment)))
    peak = float(np.max(np.abs(segment)))
    result: dict[str, float | int] = {
        "start_seconds": start,
        "end_seconds": end,
        "duration_seconds": end - start,
        "rms_dbfs": 20 * math.log10(max(rms, 1e-12)),
        "peak_dbfs": 20 * math.log10(max(peak, 1e-12)),
        "voiced_frames": int(pitches.size),
    }
    if pitches.size:
        result.update(
            {
                "f0_median_hz": float(np.median(pitches)),
                "f0_p10_hz": float(np.percentile(pitches, 10)),
                "f0_p90_hz": float(np.percentile(pitches, 90)),
            }
        )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--region", action="append", required=True, help="START:END")
    parser.add_argument("--sample-rate", type=int, default=48000)
    args = parser.parse_args()

    audio = read_mono_f32(args.input, args.sample_rate)
    regions = []
    for value in args.region:
        start_text, end_text = value.split(":", 1)
        regions.append(analyze_region(audio, args.sample_rate, float(start_text), float(end_text)))

    comparison: dict[str, float] = {}
    if len(regions) == 2 and all("f0_median_hz" in region for region in regions):
        first = float(regions[0]["f0_median_hz"])
        second = float(regions[1]["f0_median_hz"])
        comparison["median_f0_difference_semitones"] = 12 * math.log2(second / first)
        comparison["rms_difference_db"] = float(regions[1]["rms_dbfs"]) - float(regions[0]["rms_dbfs"])

    print(json.dumps({"regions": regions, "comparison": comparison}, indent=2))


if __name__ == "__main__":
    main()

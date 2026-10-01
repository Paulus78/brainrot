"""Grundfrequenz-Messung ohne Zusatzabhaengigkeiten (Autokorrelation)."""
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np


def load_mono(path, sr=22050):
    """Datei ueber ffmpeg als Mono-Float laden."""
    out = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"],
        capture_output=True, check=True,
    ).stdout
    x = np.frombuffer(out, np.int16).astype(np.float32) / 32768.0
    return x, sr


def f0_track(x, sr, fmin=70, fmax=700, frame=0.040, hop=0.010):
    n = int(frame * sr)
    h = int(hop * sr)
    lo, hi = int(sr / fmax), int(sr / fmin)
    out = []
    win = np.hanning(n)
    for i in range(0, max(0, len(x) - n), h):
        seg = x[i:i + n]
        rms = float(np.sqrt((seg ** 2).mean()))
        if rms < 0.012:
            continue
        s = (seg - seg.mean()) * win
        ac = np.correlate(s, s, "full")[n - 1:]
        if ac[0] <= 0:
            continue
        ac /= ac[0]
        band = ac[lo:hi]
        if len(band) == 0:
            continue
        k = int(np.argmax(band)) + lo
        if ac[k] < 0.35:
            continue
        out.append((i / sr, sr / k, rms, ac[k]))
    return out


def summarize(path):
    x, sr = load_mono(path)
    tr = f0_track(x, sr)
    dur = len(x) / sr
    if not tr:
        return {"file": str(path), "dur": round(dur, 2), "voiced": 0}
    fs = np.array([t[1] for t in tr])
    return {
        "file": Path(path).name, "dur": round(dur, 2), "voiced_frames": len(tr),
        "f0_median": round(float(np.median(fs)), 1),
        "f0_p10": round(float(np.percentile(fs, 10)), 1),
        "f0_p90": round(float(np.percentile(fs, 90)), 1),
    }


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(summarize(p))

#!/usr/bin/env python3
"""Build the 12-second continuity-first V2 Bongo Bucket pilot."""

from pathlib import Path
import os
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "episodes" / "pilot_001" / "revision_v2" / "video_raw"
OUTPUT = ROOT / "output" / "pilot_001" / "revision_v2" / "pilot_001_v2_final.mp4"

# Each tuple is: source file, useful source duration, final edit duration.
# Video and audio are accelerated together; atempo preserves vocal pitch.
SHOTS = [
    (RAW / "shot_01_broken_fan_retry.mp4", 2.90, 2.40),
    (RAW / "shot_02_fan_and_banana_enter_retry.mp4", 3.85, 2.60),
    (RAW / "shot_03_three_shakes.mp4", 3.30, 2.70),
    (RAW / "shot_04_repaired_fan_exits.mp4", 4.00, 2.50),
    (RAW / "shot_05_working_payoff.mp4", 3.20, 1.80),
]


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
    raise SystemExit("ffmpeg was not found. Install it or set the FFMPEG environment variable.")


def main() -> None:
    missing = [str(path) for path, _, _ in SHOTS if not path.is_file()]
    if missing:
        raise SystemExit("Missing accepted V2 source renders:\n" + "\n".join(missing))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    ffmpeg = find_ffmpeg()

    filter_parts: list[str] = []
    concat_inputs: list[str] = []
    for index, (_, source_duration, final_duration) in enumerate(SHOTS):
        speed = source_duration / final_duration
        filter_parts.extend(
            [
                f"[{index}:v]trim=start=0:end={source_duration:.3f},"
                f"setpts=(PTS-STARTPTS)/{speed:.9f},fps=24,format=yuv420p[v{index}]",
                f"[{index}:a]atrim=start=0:end={source_duration:.3f},"
                f"asetpts=PTS-STARTPTS,atempo={speed:.9f},aresample=48000[a{index}]",
            ]
        )
        concat_inputs.extend([f"[v{index}]", f"[a{index}]"])

    filter_parts.append(
        "".join(concat_inputs)
        + f"concat=n={len(SHOTS)}:v=1:a=1[vmain][amixed]"
    )
    filter_parts.append(
        "[amixed]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,"
        "loudnorm=I=-16:LRA=9:TP=-1.5,aresample=48000,"
        "aformat=sample_fmts=fltp:channel_layouts=stereo,"
        "alimiter=limit=0.95,atrim=start=0:end=12[aout]"
    )
    filters = ";".join(filter_parts)

    command = [ffmpeg, "-y"]
    for source, _, _ in SHOTS:
        command.extend(["-i", str(source)])
    command.extend(
        [
            "-filter_complex",
            filters,
            "-map",
            "[vmain]",
            "-map",
            "[aout]",
            "-r",
            "24",
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            "-t",
            "12",
            str(OUTPUT),
        ]
    )
    subprocess.run(command, check=True)
    print(OUTPUT)


if __name__ == "__main__":
    main()

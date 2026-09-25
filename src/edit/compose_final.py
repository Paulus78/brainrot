#!/usr/bin/env python3
"""Build the 12-second Bongo Bucket pilot from the accepted Flow renders."""

from pathlib import Path
import os
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "episodes" / "pilot_001" / "video_raw"
OUTPUT = ROOT / "output" / "pilot_001" / "pilot_001_final.mp4"

INPUTS = [
    RAW / "shot_01_problem_omni_voice_attempt_01.mp4",
    RAW / "shot_02_bucketo_omni_voice_attempt_01.mp4",
    RAW / "shot_03_banga_omni_voice_attempt_02.mp4",
    RAW / "shot_04_reveal_omni_voice_attempt_04.mp4",
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
    missing = [str(path) for path in INPUTS if not path.is_file()]
    if missing:
        raise SystemExit("Missing accepted source renders:\n" + "\n".join(missing))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    ffmpeg = find_ffmpeg()

    # Editorial timing follows the approved ranges in PILOT_EPISODE.md:
    # 2.5 s problem, 2.0 s bucket, 3.0 s ritual, 4.5 s reveal = 12.0 s.
    # The final reveal freezes for 0.5 s so the dry catchphrase has room to land.
    filters = """
[0:v]trim=start=0:end=2.5,setpts=PTS-STARTPTS[v0];
[0:a]atrim=start=0:end=2.5,asetpts=PTS-STARTPTS[a0];
[1:v]trim=start=0:end=2.0,setpts=PTS-STARTPTS[v1];
[1:a]atrim=start=0:end=2.0,asetpts=PTS-STARTPTS[a1];
[2:v]trim=start=0:end=3.0,setpts=PTS-STARTPTS[v2];
[2:a]atrim=start=0:end=3.0,asetpts=PTS-STARTPTS[a2];
[3:v]trim=start=0:end=4.0,setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=0.5[v3];
[3:a]atrim=start=0:end=4.0,asetpts=PTS-STARTPTS,apad=pad_dur=0.5,atrim=start=0:end=4.5[a3];
[v0][a0][v1][a1][v2][a2][v3][a3]concat=n=4:v=1:a=1[vmain][amain];
[amain]aresample=48000[voice];
sine=frequency=105:sample_rate=48000:duration=0.13,afade=t=out:st=0:d=0.13,volume=0.055,adelay=5180|5180,aformat=channel_layouts=stereo[hit1];
sine=frequency=95:sample_rate=48000:duration=0.15,afade=t=out:st=0:d=0.15,volume=0.075,adelay=5950|5950,aformat=channel_layouts=stereo[hit2];
sine=frequency=82:sample_rate=48000:duration=0.19,afade=t=out:st=0:d=0.19,volume=0.11,adelay=6960|6960,aformat=channel_layouts=stereo[hit3];
sine=frequency=659.25:sample_rate=48000:duration=0.13,afade=t=out:st=0:d=0.13,volume=0.035,adelay=7520|7520,aformat=channel_layouts=stereo[logo1];
sine=frequency=880:sample_rate=48000:duration=0.18,afade=t=out:st=0:d=0.18,volume=0.028,adelay=7690|7690,aformat=channel_layouts=stereo[logo2];
anoisesrc=color=pink:sample_rate=48000:duration=4.5,highpass=f=250,lowpass=f=1800,volume=0.018,afade=t=in:st=0:d=0.45,afade=t=out:st=4.0:d=0.5,adelay=7500|7500,aformat=channel_layouts=stereo[wind];
[voice][hit1][hit2][hit3][logo1][logo2][wind]amix=inputs=7:duration=longest,loudnorm=I=-16:LRA=9:TP=-1.5,aresample=48000,alimiter=limit=0.95,atrim=start=0:end=12[aout]
""".replace("\n", "")

    command = [ffmpeg, "-y"]
    for source in INPUTS:
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

#!/usr/bin/env python3
"""Build the 15-second silent storyboard animatic for Bongo Popcorno."""

from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[2]
SIZE = (1080, 1920)
OUTPUT_DIR = ROOT / "output" / "pilot_002"
WEBP_OUTPUT = OUTPUT_DIR / "pilot_002_silent_animatic.webp"
GIF_OUTPUT = OUTPUT_DIR / "pilot_002_silent_animatic.gif"

# These durations match the approved four-beat structure and total 15 seconds.
SHOTS = [
    (ROOT / "episodes/pilot_002/keyframes/frame_01_tooth_ping.png", 3000),
    (ROOT / "episodes/pilot_002/keyframes/frame_02_banana_drop.png", 4000),
    (ROOT / "episodes/pilot_002/keyframes/frame_03_planted_bucket_tap.png", 3500),
    (ROOT / "episodes/pilot_002/keyframes/frame_04_banana_popcorn_payoff.png", 4500),
]


def load_frame(path: Path) -> Image.Image:
    if not path.is_file():
        raise SystemExit(f"Missing approved storyboard frame: {path}")
    with Image.open(path) as source:
        return ImageOps.fit(source.convert("RGB"), SIZE, method=Image.Resampling.LANCZOS)


def main() -> None:
    frames = [load_frame(path) for path, _ in SHOTS]
    durations = [duration for _, duration in SHOTS]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    frames[0].save(
        WEBP_OUTPUT,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        lossless=True,
        method=6,
    )

    gif_frames = [
        frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=256)
        for frame in frames
    ]
    gif_frames[0].save(
        GIF_OUTPUT,
        save_all=True,
        append_images=gif_frames[1:],
        duration=durations,
        loop=0,
        optimize=False,
        disposal=2,
    )

    print(WEBP_OUTPUT)
    print(GIF_OUTPUT)


if __name__ == "__main__":
    main()

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[2]
SIZE = (1080, 1920)
WEBP_OUTPUT = ROOT / "output/pilot_001/pilot_001_animatic.webp"
GIF_OUTPUT = ROOT / "output/pilot_001/pilot_001_animatic.gif"

SHOTS = [
    (ROOT / "episodes/pilot_001/keyframes/shot_01_problem.png", 2000, None),
    (ROOT / "episodes/pilot_001/keyframes/shot_02_bucketo.png", 2000, None),
    (ROOT / "episodes/pilot_001/keyframes/shot_03_banga.png", 3000, None),
    (ROOT / "episodes/pilot_001/keyframes/shot_04_reveal.png", 5000, None),
]


def load_frame(path: Path, label: str | None) -> Image.Image:
    with Image.open(path) as source:
        frame = ImageOps.fit(source.convert("RGB"), SIZE, method=Image.Resampling.LANCZOS)

    if label:
        draw = ImageDraw.Draw(frame, "RGBA")
        draw.rectangle((0, 1610, 1080, 1760), fill=(0, 0, 0, 185))
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 46)
        except OSError:
            font = ImageFont.load_default()
        box = draw.textbbox((0, 0), label, font=font)
        text_width = box[2] - box[0]
        draw.text(((1080 - text_width) / 2, 1655), label, font=font, fill=(255, 255, 255, 255))
    return frame


frames = [load_frame(path, label) for path, _, label in SHOTS]
durations = [duration for _, duration, _ in SHOTS]
WEBP_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
frames[0].save(
    WEBP_OUTPUT,
    save_all=True,
    append_images=frames[1:],
    duration=durations,
    loop=0,
    lossless=True,
    method=6,
)
gif_frames = [frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=256) for frame in frames]
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

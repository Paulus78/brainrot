from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[2]
SIZE = (1080, 1920)
OUTPUT_DIR = ROOT / "output" / "pilot_001" / "revision_v2"
WEBP_OUTPUT = OUTPUT_DIR / "pilot_001_v2_animatic.webp"
GIF_OUTPUT = OUTPUT_DIR / "pilot_001_v2_animatic.gif"

SHOTS = [
    (ROOT / "episodes/pilot_001/revision_v2/keyframes/shot_01_broken_fan.jpg", 2500),
    (ROOT / "episodes/pilot_001/revision_v2/keyframes/shot_02_fan_over_bucket.jpg", 2500),
    (ROOT / "episodes/pilot_001/revision_v2/keyframes/shot_03_banga_loaded_bucket.jpg", 3000),
    (ROOT / "episodes/pilot_001/revision_v2/keyframes/shot_04_repaired_fan_emerging.jpg", 2000),
    (ROOT / "episodes/pilot_001/revision_v2/keyframes/shot_05_working_fan_start.jpg", 2000),
]


def load_frame(path: Path) -> Image.Image:
    with Image.open(path) as source:
        return ImageOps.fit(source.convert("RGB"), SIZE, method=Image.Resampling.LANCZOS)


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

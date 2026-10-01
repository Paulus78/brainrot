"""Rendert den Short: Frames parallel -> ffmpeg (H.264) + Audio-Mix -> MP4, dazu Kontaktbogen.

  python src/anim/render.py --tag v01
"""
import argparse
import multiprocessing as mp
import subprocess
import sys
import time
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output" / "ep004"
_CTX = None


def _init():
    global _CTX
    import story
    _CTX = story.Ctx()


def _frame(i):
    import story
    from engine import FPS
    return i, story.render_frame(i / FPS, _CTX)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="v01")
    ap.add_argument("--audio", default=None)
    ap.add_argument("--workers", type=int, default=max(1, (mp.cpu_count() or 4) - 1))
    ap.add_argument("--sheet-count", type=int, default=24)
    args = ap.parse_args()

    import timeline as TL
    from engine import FPS, W, H
    OUT.mkdir(parents=True, exist_ok=True)
    n = int(round(TL.T_END * FPS))
    video = OUT / f"bongo_test_{args.tag}_silent.mp4"
    final = OUT / f"bongo_test_{args.tag}.mp4"
    audio = Path(args.audio) if args.audio else TL.EP / "audio" / f"mix_{args.tag}.wav"

    # 1) Frames -> stiller Videostream
    ff = subprocess.Popen(
        ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(video)],
        stdin=subprocess.PIPE)
    t0 = time.time()
    keep = {}
    sheet_idx = set(np.linspace(0, n - 1, args.sheet_count).astype(int).tolist())
    with mp.Pool(args.workers, initializer=_init) as pool:
        for done, (i, fr) in enumerate(pool.imap(_frame, range(n), chunksize=2)):
            ff.stdin.write(fr.tobytes())
            if i in sheet_idx:
                keep[i] = cv2.resize(fr, None, fx=0.22, fy=0.22, interpolation=cv2.INTER_AREA)
            if done % 30 == 0:
                print(f"  frame {done}/{n}  {time.time() - t0:.0f}s", flush=True)
    ff.stdin.close()
    ff.wait()
    print(f"frames done in {time.time() - t0:.0f}s")

    # 2) Kontaktbogen
    tiles = []
    for i in sorted(keep):
        tl = keep[i].copy()
        cv2.rectangle(tl, (0, 0), (52, 16), (0, 0, 0), -1)
        cv2.putText(tl, f"{i / FPS:.2f}", (3, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 255), 1, cv2.LINE_AA)
        tiles.append(tl)
    cols = 8
    while len(tiles) % cols:
        tiles.append(np.zeros_like(tiles[0]))
    sheet = np.vstack([np.hstack(tiles[i:i + cols]) for i in range(0, len(tiles), cols)])
    sheet_path = OUT / f"bongo_test_{args.tag}_contactsheet.jpg"
    cv2.imwrite(str(sheet_path), sheet, [cv2.IMWRITE_JPEG_QUALITY, 90])

    # 3) Mux mit Audio (H.264 + AAC)
    if audio.exists():
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", str(video), "-i", str(audio),
             "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000",
             "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{TL.T_END:.3f}", "-movflags", "+faststart", str(final)],
            check=True)
        print("final:", final)
    print("sheet:", sheet_path)


if __name__ == "__main__":
    mp.freeze_support()
    main()

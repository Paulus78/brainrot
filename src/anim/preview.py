"""Einzelne Zeitpunkte rendern und als Kontaktbogen speichern.

  python src/anim/preview.py out.png 0.1 0.5 1.2 ...   (Zeiten in s)
  python src/anim/preview.py out.png --range 0 3 0.25
"""
import sys
import time
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import story  # noqa: E402


def main():
    out = sys.argv[1]
    args = sys.argv[2:]
    cols = 6
    if "--cols" in args:
        i = args.index("--cols")
        cols = int(args[i + 1])
        del args[i:i + 2]
    scale = 0.30
    if "--scale" in args:
        i = args.index("--scale")
        scale = float(args[i + 1])
        del args[i:i + 2]
    if args and args[0] == "--range":
        a, b, s = map(float, args[1:4])
        times = list(np.arange(a, b + 1e-6, s))
    else:
        times = [float(x) for x in args]
    ctx = story.Ctx()
    tiles = []
    t0 = time.time()
    for t in times:
        f = story.render_frame(t, ctx)
        tile = cv2.resize(f, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        cv2.rectangle(tile, (0, 0), (74, 22), (0, 0, 0), -1)
        cv2.putText(tile, f"{t:.2f}s", (4, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        tiles.append(tile)
    print(f"{len(times)} frames in {time.time() - t0:.1f}s ({(time.time() - t0) / len(times):.2f}s/frame)")
    h, w = tiles[0].shape[:2]
    while len(tiles) % cols:
        tiles.append(np.zeros_like(tiles[0]))
    rows = [np.hstack(tiles[i:i + cols]) for i in range(0, len(tiles), cols)]
    cv2.imwrite(out, np.vstack(rows))
    print("->", out)


if __name__ == "__main__":
    main()

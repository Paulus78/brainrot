"""Freistellen der Bongo-Referenz und Zerlegung in animierbare Layer.

Ausgabe nach assets/rig/ als RGBA-PNGs plus work/debug_*.png zur Kontrolle.
"""
from pathlib import Path

import cv2
import numpy as np
from scipy import ndimage as ndi

ROOT = Path(__file__).resolve().parents[2]
REF = ROOT / "assets" / "character_master" / "bongo_reference.png"
OUT = ROOT / "assets" / "rig"
WORK = ROOT / "work"


def saturation(rgb: np.ndarray) -> np.ndarray:
    f = rgb.astype(np.float32)
    mx = f.max(2)
    mn = f.min(2)
    return (mx - mn) / np.maximum(mx, 1.0)


def luminance(rgb: np.ndarray) -> np.ndarray:
    f = rgb.astype(np.float32)
    return 0.299 * f[..., 0] + 0.587 * f[..., 1] + 0.114 * f[..., 2]


def keep_largest(mask: np.ndarray) -> np.ndarray:
    lab, n = ndi.label(mask)
    if n == 0:
        return mask
    sizes = ndi.sum(mask, lab, range(1, n + 1))
    return lab == (int(np.argmax(sizes)) + 1)


def rgba(rgb: np.ndarray, mask: np.ndarray, feather: float = 0.9) -> np.ndarray:
    a = (mask.astype(np.float32) * 255.0)
    if feather > 0:
        a = cv2.GaussianBlur(a, (0, 0), feather)
    out = np.dstack([rgb, a.clip(0, 255).astype(np.uint8)])
    return out


def save(arr: np.ndarray, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path), cv2.cvtColor(arr, cv2.COLOR_RGBA2BGRA))


def crop_rgba(arr: np.ndarray):
    ys, xs = np.nonzero(arr[..., 3] > 8)
    if len(ys) == 0:
        return arr, (0, 0)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    return arr[y0:y1, x0:x1], (int(x0), int(y0))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)

    rgb = np.asarray(cv2.cvtColor(cv2.imread(str(REF)), cv2.COLOR_BGR2RGB))
    H, W, _ = rgb.shape
    sat = saturation(rgb)
    lum = luminance(rgb)

    # --- Grundkoerper ueber Saettigung (Hintergrund ist fast grau) ---
    core = sat > 0.25
    core = ndi.binary_opening(core, np.ones((3, 3)))
    core = keep_largest(core)
    core = ndi.binary_closing(core, np.ones((7, 7)))
    body = ndi.binary_fill_holes(core)  # Augen, Mund, Smiley, Nase werden gefuellt

    # --- Gelbmaske: Banane (oben) und Eimer (unten) ---
    r, g, b = rgb[..., 0].astype(np.float32), rgb[..., 1].astype(np.float32), rgb[..., 2].astype(np.float32)
    yellow = (sat > 0.55) & (r > 150) & (g > 110) & (b < 140) & (r > b + 70) & (g > b + 50)
    yellow = ndi.binary_opening(yellow, np.ones((5, 5)))
    lab_y, n_y = ndi.label(yellow)
    comps = []
    for i in range(1, n_y + 1):
        m = lab_y == i
        if m.sum() < 2000:
            continue
        ys, xs = np.nonzero(m)
        comps.append((m.sum(), ys.mean(), m))
    comps.sort(key=lambda c: -c[0])
    banana = next((c[2] for c in comps if c[1] < H * 0.45), np.zeros_like(yellow))
    bucket_y = next((c[2] for c in comps if c[1] > H * 0.55), np.zeros_like(yellow))

    banana = ndi.binary_fill_holes(ndi.binary_closing(banana, np.ones((9, 9))))
    bucket_y = ndi.binary_fill_holes(ndi.binary_closing(bucket_y, np.ones((9, 9))))

    # --- Eimer-Buegel: dunkler, wenig gesaettigter Bogen ueber dem Eimer ---
    ys, xs = np.nonzero(bucket_y)
    bx0, bx1, by0, by1 = xs.min(), xs.max(), ys.min(), ys.max()
    zone = np.zeros_like(bucket_y)
    zone[max(0, by0 - 170):by0 + 60, max(0, bx0 - 30):bx1 + 30] = True
    handle = zone & (lum < 150) & (sat < 0.45) & ~body
    handle = ndi.binary_closing(handle, np.ones((5, 5)))
    handle = ndi.binary_opening(handle, np.ones((3, 3)))
    # nur groessere Fragmente behalten
    lab_h, n_h = ndi.label(handle)
    keep = np.zeros_like(handle)
    for i in range(1, n_h + 1):
        m = lab_h == i
        if m.sum() > 400:
            keep |= m
    handle = keep

    bucket = bucket_y | handle
    bucket = ndi.binary_closing(bucket, np.ones((5, 5)))

    full = body | bucket

    # --- Debug ---
    dbg = rgb.copy()
    dbg[body] = (dbg[body] * 0.55 + np.array([0, 255, 0]) * 0.45).astype(np.uint8)
    dbg[banana] = (dbg[banana] * 0.4 + np.array([255, 0, 255]) * 0.6).astype(np.uint8)
    dbg[bucket_y] = (dbg[bucket_y] * 0.4 + np.array([0, 128, 255]) * 0.6).astype(np.uint8)
    dbg[handle] = np.array([255, 0, 0])
    cv2.imwrite(str(WORK / "debug_masks.png"), cv2.cvtColor(dbg, cv2.COLOR_RGB2BGR))

    save(rgba(rgb, full), OUT / "_full.png")
    save(rgba(rgb, bucket), OUT / "_bucket.png")
    save(rgba(rgb, banana), OUT / "_banana.png")

    print("full bbox", np.nonzero(full)[1].min(), np.nonzero(full)[0].min(),
          np.nonzero(full)[1].max(), np.nonzero(full)[0].max())
    print("bucket bbox", bx0, by0, bx1, by1, "handle px", int(handle.sum()))
    ys, xs = np.nonzero(banana)
    print("banana bbox", xs.min(), ys.min(), xs.max(), ys.max())

    # --- Augen + Mund: gefuellte Loecher innerhalb des Kopfes ---
    holes = body & ~core
    lab_o, n_o = ndi.label(holes)
    info = []
    for i in range(1, n_o + 1):
        m = lab_o == i
        n = int(m.sum())
        if n < 500:
            continue
        ys, xs = np.nonzero(m)
        info.append((n, int(xs.mean()), int(ys.mean()), int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())))
    info.sort(key=lambda t: -t[0])
    print("holes (size, cx, cy, x0,y0,x1,y1):")
    for t in info[:8]:
        print("  ", t)


if __name__ == "__main__":
    main()

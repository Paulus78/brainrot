"""Zerlegt die Bongo-Referenz in animierbare Rig-Layer.

Alles wird aus assets/character_master/bongo_reference.png berechnet.
Ergebnis: assets/rig/*.png + assets/rig/rig.json

Layer
  torso.png        Rumpf, Arme, Beine, ohne Eimer (Handloch inpainted)
  head.png         Kopf, Ohren, Banane, Augen/Mund herausretuschiert
  bucket.png       nur der gelbe Eimer (Buegel wird prozedural gezeichnet)
  eyeL/R_white.png Augapfel ohne Iris
  eyeL/R_iris.png  Iris + Pupille, frei verschiebbar
  tooth.png        der eine grosse Frontzahn
"""
import json
from pathlib import Path

import cv2
import numpy as np
from scipy import ndimage as ndi

ROOT = Path(__file__).resolve().parents[2]
REF = ROOT / "assets" / "character_master" / "bongo_reference.png"
OUT = ROOT / "assets" / "rig"
WORK = ROOT / "work"

NECK_Y = 895
HEAD_BOTTOM = NECK_Y + 75
TORSO_TOP = NECK_Y - 30


def save(arr, path):
    cv2.imwrite(str(path), cv2.cvtColor(arr, cv2.COLOR_RGBA2BGRA))


def crop(arr):
    ys, xs = np.nonzero(arr[..., 3] > 4)
    y0, y1, x0, x1 = int(ys.min()), int(ys.max()) + 1, int(xs.min()), int(xs.max()) + 1
    return arr[y0:y1, x0:x1], (x0, y0)


def feather(mask, sigma=1.0):
    return cv2.GaussianBlur((mask * 255).astype(np.uint8), (0, 0), sigma)


def vfade(alpha, y_edge, fade, keep_above):
    h = alpha.shape[0]
    y = np.arange(h, dtype=np.float32)
    t = (y - (y_edge - fade)) / fade if keep_above else ((y_edge + fade) - y) / fade
    ramp = 1.0 - np.clip(t, 0.0, 1.0)
    return (alpha.astype(np.float32) * ramp[:, None]).astype(np.uint8)


def inpaint(rgb, mask, radius=9):
    out = cv2.inpaint(cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR), mask.astype(np.uint8), radius, cv2.INPAINT_TELEA)
    return cv2.cvtColor(out, cv2.COLOR_BGR2RGB)



def defringe(layer):
    """Randpixel bekommen die Farbe des Fells/Eimers von innen (kein heller Hintergrund-Halo)
    und die Alpha-Kante wird 1px nach innen gezogen."""
    a = layer[..., 3]
    interior = ndi.binary_erosion(a > 250, iterations=3)
    w = interior.astype(np.float32)
    rgb = layer[..., :3].astype(np.float32)
    num = cv2.GaussianBlur(rgb * w[..., None], (0, 0), 4)
    den = cv2.GaussianBlur(w, (0, 0), 4)[..., None]
    fill = num / np.maximum(den, 1e-3)
    out = layer.copy()
    band = ~interior & (den[..., 0] > 0.02)
    out[..., :3][band] = np.clip(fill[band], 0, 255).astype(np.uint8)
    a2 = cv2.erode(a, np.ones((3, 3), np.uint8))
    out[..., 3] = cv2.GaussianBlur(a2, (0, 0), 0.7)
    return out

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)

    rgb = cv2.cvtColor(cv2.imread(str(REF)), cv2.COLOR_BGR2RGB)
    H, W, _ = rgb.shape
    f = rgb.astype(np.float32)
    lum = 0.299 * f[..., 0] + 0.587 * f[..., 1] + 0.114 * f[..., 2]
    sat = (f.max(2) - f.min(2)) / np.maximum(f.max(2), 1.0)

    # ---- Grundmaske ueber Saettigung ----
    core = sat > 0.25
    core = ndi.binary_closing(ndi.binary_opening(core, np.ones((3, 3))), np.ones((7, 7)))
    lab, n = ndi.label(core)
    core = lab == int(np.argmax(ndi.sum(core, lab, range(1, n + 1)))) + 1

    # Loecher fuellen, aber Hintergrund-Loecher (z.B. unter dem Eimerbuegel) verwerfen
    filled = ndi.binary_fill_holes(core)
    holes = filled & ~core
    lab_h, n_h = ndi.label(holes)
    char = core.copy()
    face_holes = []
    for i in range(1, n_h + 1):
        m = lab_h == i
        ys, xs = np.nonzero(m)
        cy = ys.mean()
        if cy > 950 and lum[m].mean() > 140 and sat[m].mean() < 0.18:
            continue  # Hintergrund unter dem Buegel
        char |= m
        if m.sum() >= 2000 and cy < 950:
            face_holes.append((int(m.sum()), m, [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1],
                               [float(xs.mean()), float(cy)]))
    face_holes.sort(key=lambda t: -t[0])

    meta = {"source_size": [W, H], "fps_note": "Koordinaten im Referenz-Bildraum"}

    # ---- Eimer (nur Gelb, unten) ----
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    yellow = (sat > 0.55) & (r > 150) & (g > 110) & (b < 140) & (r > b + 70) & (g > b + 50)
    yellow = ndi.binary_opening(yellow, np.ones((5, 5)))
    lab_y, n_y = ndi.label(yellow)
    bmask = np.zeros_like(yellow)
    best = 0
    for i in range(1, n_y + 1):
        m = lab_y == i
        ys, _ = np.nonzero(m)
        if m.sum() > best and ys.mean() > H * 0.55:
            best, bmask = int(m.sum()), m
    bmask = ndi.binary_fill_holes(ndi.binary_closing(bmask, np.ones((9, 9))))
    # Faust am Buegel gehoert zum Eimer (liegt im Original ueber dem Buegel)
    fist = np.zeros_like(bmask)
    fist[968:1066, 640:748] = True
    fist &= core & ~ndi.binary_dilation(bmask, np.ones((3, 3)))
    fist = ndi.binary_closing(fist, np.ones((5, 5)))
    unit = bmask | fist
    bucket_rgba = np.dstack([rgb, feather(unit, 1.0)])
    bcrop, borig = crop(bucket_rgba)
    bcrop = defringe(bcrop)
    save(bcrop, OUT / "bucket.png")
    bys, bxs = np.nonzero(bmask)
    # Rim: oberste Zeile mit nennenswerter Breite
    rim_y = int(bys.min())
    row_w = bmask.sum(1)
    rim_y = int(np.argmax(row_w > row_w.max() * 0.85))
    meta["bucket"] = {
        "origin": list(borig), "size": [int(bcrop.shape[1]), int(bcrop.shape[0])],
        "rim_y": rim_y,
        "rim_x0": int(np.nonzero(bmask[rim_y])[0].min()),
        "rim_x1": int(np.nonzero(bmask[rim_y])[0].max()),
        "bottom_y": int(bys.max()), "cx": float(bxs.mean()),
    }

    # ---- Torso (ohne Eimer, Handloch inpainted) ----
    bmask_d = ndi.binary_dilation(bmask, np.ones((7, 7)))
    body_mask = char & ~bmask_d
    body_mask = ndi.binary_opening(body_mask, np.ones((3, 3)))
    lab_b, n_b = ndi.label(body_mask)
    body_mask = lab_b == int(np.argmax(ndi.sum(body_mask, lab_b, range(1, n_b + 1)))) + 1
    # Fehlende Hand hinter dem Eimer grob ergaenzen
    patch = bmask_d & ndi.binary_dilation(body_mask, np.ones((31, 31)))
    body_ext = body_mask | patch
    src_for_fill = rgb.copy()
    src_for_fill[~body_mask] = 0
    body_rgb = inpaint(src_for_fill, patch & ~body_mask, 11)

    # Rand-Artefakte am Eimer (dunkle Schattenfetzen, gelbe Splitter) entfernen
    yellow_any = (g / np.maximum(r, 1) > 0.76) & (b < 0.55 * r) & (r > 150)
    yellow_any = ndi.binary_dilation(yellow_any, np.ones((9, 9)))
    body_ext &= ~yellow_any
    cut = np.zeros_like(body_ext)
    cut[1112:1300, 590:] = True           # rechts vom Bauch, unterhalb der Faust
    cut[1300:, 614:] = True               # Fussrand frei lassen, Eimerschatten weg
    body_ext &= ~cut
    body_ext = ndi.binary_opening(body_ext, np.ones((5, 5)))
    lab_t, n_t = ndi.label(body_ext)
    body_ext = lab_t == int(np.argmax(ndi.sum(body_ext, lab_t, range(1, n_t + 1)))) + 1
    torso_a = vfade(feather(body_ext, 1.0), TORSO_TOP, 30, keep_above=False)
    tcrop, torig = crop(np.dstack([body_rgb, torso_a]))
    tcrop = defringe(tcrop)
    save(tcrop, OUT / "torso.png")
    meta["torso"] = {"origin": list(torig), "size": [int(tcrop.shape[1]), int(tcrop.shape[0])]}

    # ---- Augen ----
    ell = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41))
    eye_feats = [t for t in face_holes if t[3][1] < 858][:2]
    eye_feats.sort(key=lambda t: t[3][0])
    mouth_feat = next((t for t in face_holes if t[3][1] >= 855), None)

    remove = np.zeros((H, W), bool)
    eye_masks = []
    meta["eyes"] = []
    eye_data = []
    for idx, (_, m, bbox, c) in enumerate(eye_feats):
        em = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, ell).astype(bool)
        em = ndi.binary_fill_holes(em)
        remove |= em
        eye_masks.append(em)
        x0, y0, x1, y1 = bbox
        pad = 14
        x0, y0 = max(0, x0 - pad), max(0, y0 - pad)
        x1, y1 = min(W, x1 + pad), min(H, y1 + pad)
        sub = rgb[y0:y1, x0:x1]
        sm = em[y0:y1, x0:x1]
        sl = lum[y0:y1, x0:x1]
        iris = sm & (sl < 185)
        iris = ndi.binary_fill_holes(ndi.binary_opening(iris, np.ones((5, 5))))
        lab_i, n_i = ndi.label(iris)
        if n_i:
            iris = lab_i == int(np.argmax(ndi.sum(iris, lab_i, range(1, n_i + 1)))) + 1

        white_rgb = inpaint(sub, ndi.binary_dilation(iris, np.ones((7, 7))), 9)
        white = np.dstack([white_rgb, feather(sm, 1.0)])
        iris_rgba = np.dstack([sub, feather(iris, 1.0)])
        icrop, iorig = crop(iris_rgba)

        name = "eyeL" if idx == 0 else "eyeR"
        save(white, OUT / f"{name}_white.png")
        save(icrop, OUT / f"{name}_iris.png")
        ys, xs = np.nonzero(sm)
        iys, ixs = np.nonzero(iris)
        d = {
            "name": name,
            "white_origin": [x0, y0], "white_size": [int(sm.shape[1]), int(sm.shape[0])],
            "center": [x0 + float(xs.mean()), y0 + float(ys.mean())],
            "half": [float(xs.max() - xs.min()) / 2, float(ys.max() - ys.min()) / 2],
            "top": y0 + int(ys.min()), "bottom": y0 + int(ys.max()),
            "left": x0 + int(xs.min()), "right": x0 + int(xs.max()),
            "iris_origin": [x0 + iorig[0], y0 + iorig[1]],
            "iris_size": [int(icrop.shape[1]), int(icrop.shape[0])],
            "iris_center": [x0 + float(ixs.mean()), y0 + float(iys.mean())],
        }
        meta["eyes"].append(d)
        eye_data.append(d)
        print(name, {k: v for k, v in d.items() if k != "name"})

    # ---- Mund / Zahn ----
    if mouth_feat is not None:
        _, m, bbox, c = mouth_feat
        remove |= m
        x0, y0, x1, y1 = bbox
        pad = 8
        x0, y0 = max(0, x0 - pad), max(0, y0 - pad)
        x1, y1 = min(W, x1 + pad), min(H, y1 + pad)
        tooth = np.dstack([rgb[y0:y1, x0:x1], feather(m[y0:y1, x0:x1], 0.8)])
        tc, to = crop(tooth)
        save(tc, OUT / "tooth.png")
        meta["mouth"] = {"tooth_origin": [x0 + to[0], y0 + to[1]],
                         "tooth_size": [int(tc.shape[1]), int(tc.shape[0])],
                         "center": [round(c[0], 1), round(c[1], 1)]}
        # Mundhoehle: dunkle Pixel um den Zahn herum
        zone = np.zeros((H, W), bool)
        zone[int(c[1]) - 55:int(c[1]) + 60, int(c[0]) - 95:int(c[0]) + 95] = True
        dark = zone & core & (lum < 95)
        if dark.sum() > 200:
            dys, dxs = np.nonzero(dark)
            meta["mouth"]["cavity"] = [int(dxs.min()), int(dys.min()), int(dxs.max()), int(dys.max())]
            remove |= ndi.binary_dilation(dark, np.ones((5, 5)))
        print("mouth", meta["mouth"])

    # ---- Kopf ohne Augen/Mund ----
    head_rgb = inpaint(rgb, ndi.binary_dilation(remove, np.ones((9, 9))), 11)
    # linkes Auge: Loch mit echtem Fell (Bauch) seamless fuellen -> Lider werden reine Transparenz
    emL = ndi.binary_dilation(eye_masks[0], np.ones((37, 37)))
    ys_, xs_ = np.nonzero(emL)
    bx0, by0, bx1, by1 = int(xs_.min()), int(ys_.min()), int(xs_.max()) + 1, int(ys_.max()) + 1
    bw, bh = bx1 - bx0, by1 - by0
    belly = rgb[985:985 + bh + 40, 175:175 + bw + 40]        # sauberes Bauchfell, leicht groesser
    sub_mask = np.zeros(belly.shape[:2], np.uint8)
    sub_mask[20:20 + bh, 20:20 + bw] = (emL[by0:by1, bx0:bx1] * 255).astype(np.uint8)
    cx_, cy_ = bx0 - 20 + belly.shape[1] // 2, by0 - 20 + belly.shape[0] // 2
    bgr = cv2.cvtColor(head_rgb, cv2.COLOR_RGB2BGR)
    cl = cv2.seamlessClone(cv2.cvtColor(belly, cv2.COLOR_RGB2BGR), bgr, sub_mask, (cx_, cy_), cv2.NORMAL_CLONE)
    head_rgb = cv2.cvtColor(cl, cv2.COLOR_BGR2RGB)
    head_a = feather(char, 1.0).copy()
    head_a[HEAD_BOTTOM:] = 0
    head_a = vfade(head_a, HEAD_BOTTOM - 25, 38, keep_above=True)
    hcrop, horig = crop(np.dstack([head_rgb, head_a]))
    hcrop = defringe(hcrop)
    save(hcrop, OUT / "head.png")
    meta["head"] = {"origin": list(horig), "size": [int(hcrop.shape[1]), int(hcrop.shape[0])],
                    "neck": [470, NECK_Y]}

    # Fellfarbe (fuer Lider)
    fz = core.copy()
    fz[:620] = False
    fz[890:] = False
    fz &= ~ndi.binary_dilation(remove, np.ones((45, 45)))
    meta["fur_rgb"] = [int(v) for v in rgb[fz].mean(0)]
    meta["fur_dark_rgb"] = [int(v * 0.72) for v in rgb[fz].mean(0)]
    print("fur", meta["fur_rgb"])

    (OUT / "rig.json").write_text(json.dumps(meta, indent=2))

    # Kontrollbild: Rig wieder zusammensetzen
    prev = np.full((H, W, 3), (26, 28, 36), np.uint8)

    def blit(layer, off):
        h, w = layer.shape[:2]
        roi = prev[off[1]:off[1] + h, off[0]:off[0] + w]
        a = layer[..., 3:4].astype(np.float32) / 255
        roi[:] = (layer[..., :3] * a + roi * (1 - a)).astype(np.uint8)

    blit(tcrop, torig)
    blit(hcrop, horig)
    for d in eye_data:
        w = cv2.cvtColor(cv2.imread(str(OUT / f"{d['name']}_white.png"), cv2.IMREAD_UNCHANGED), cv2.COLOR_BGRA2RGBA)
        blit(w, d["white_origin"])
        ir = cv2.cvtColor(cv2.imread(str(OUT / f"{d['name']}_iris.png"), cv2.IMREAD_UNCHANGED), cv2.COLOR_BGRA2RGBA)
        blit(ir, d["iris_origin"])
    if "mouth" in meta:
        t = cv2.cvtColor(cv2.imread(str(OUT / "tooth.png"), cv2.IMREAD_UNCHANGED), cv2.COLOR_BGRA2RGBA)
        blit(t, meta["mouth"]["tooth_origin"])
    blit(bcrop, borig)
    cv2.imwrite(str(WORK / "rig_preview.png"), cv2.cvtColor(prev, cv2.COLOR_RGB2BGR))


if __name__ == "__main__":
    main()

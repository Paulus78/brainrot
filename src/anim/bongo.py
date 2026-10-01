"""Bongo-Rig: Raster-Layer aus der Referenz + prozedurale Augen, Lider und Mund.

draw(canvas, cam, pose) zeichnet Bongo komplett. Pose ist ein dict (siehe DEFAULT);
Expressions sind Teil-Dicts, die in Pose gemischt werden.
"""
import json
import math
from pathlib import Path

import cv2
import numpy as np

from engine import (Tm, Sm, Rm, about, blit, load_sprite, premul, clamp, lerp)

ROOT = Path(__file__).resolve().parents[2]
RIG = ROOT / "assets" / "rig"

FEET = (470.0, 1411.0)      # Referenz-Fusspunkt
NECK = (470.0, 895.0)
HIP_Y = 1250.0

# BGR-Farben
FUR = (90, 115, 181)
FUR_DARK = (52, 68, 120)
LID_BLUE = (190, 92, 30)

DEFAULT = dict(
    x=540.0, y=1370.0, s=0.7, sx=1.0, sy=1.0, rot=0.0,
    tsx=1.0, tsy=1.0,                       # Torso-Squash (Kopf folgt)
    hdx=0.0, hdy=0.0, hrot=0.0, hsx=1.0, hsy=1.0,
    earL=0.0, earR=0.0, ban=0.0,
    lookx=0.3, looky=0.4, pup=1.0, lookRx=None, lookRy=None,
    lidL=0.10, lidR=0.32, lowL=0.0, lowR=0.12, slant=0.0, escL=1.0, escR=1.0, blink=0.0,
    mo=0.10, mw=0.0, msm=0.35, tongue=0.0,
    bx=0.0, by=0.0, brot=0.0, bs=1.0, bucket=True, bucketM=None,
    soot=0.0, flash=0.0, opacity=1.0, pre_bucket=None,
)

EXPR = {
    "neutral": {},
    "suspicious": dict(lidL=0.42, lidR=0.50, lowL=0.18, lowR=0.22, slant=10, msm=-0.15, mo=0.04, pup=0.9),
    "annoyed": dict(lidL=0.38, lidR=0.42, lowL=0.10, lowR=0.12, slant=16, msm=-0.45, mo=0.05, pup=0.85),
    "realization": dict(lidL=0.0, lidR=0.0, lowL=0.0, lowR=0.0, escL=1.10, escR=1.22, pup=0.72, mo=0.32, msm=0.25),
    "confident": dict(lidL=0.24, lidR=0.34, lowL=0.14, lowR=0.20, slant=-6, msm=0.85, mo=0.14),
    "intense": dict(lidL=0.30, lidR=0.32, lowL=0.22, lowR=0.24, slant=18, pup=0.7, mo=0.42, mw=0.9, msm=-0.1),
    "shocked": dict(lidL=0.0, lidR=0.0, lowL=0.0, lowR=0.0, escL=1.16, escR=1.32, pup=0.5, mo=0.62, msm=-0.2),
    "pleased": dict(lidL=0.30, lidR=0.34, lowL=0.36, lowR=0.40, slant=-4, msm=1.0, mo=0.36, tongue=0.3),
    "smug": dict(lidL=0.46, lidR=0.52, lowL=0.12, lowR=0.16, slant=-8, msm=0.95, mo=0.06, pup=1.0),
}


def expr(name, **over):
    d = dict(EXPR[name])
    d.update(over)
    return d


def mix_expr(a, b, k):
    """Zwei Expression-Dicts (oder Namen) mischen."""
    if isinstance(a, str):
        a = EXPR[a]
    if isinstance(b, str):
        b = EXPR[b]
    keys = set(DEFAULT) & (set(a) | set(b))
    out = {}
    for key in keys:
        va = a.get(key, DEFAULT[key])
        vb = b.get(key, DEFAULT[key])
        if isinstance(va, (int, float)) and isinstance(vb, (int, float)):
            out[key] = lerp(va, vb, k)
    return out


def _smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


class Bongo:
    def __init__(self):
        self.meta = json.loads((RIG / "rig.json").read_text())
        self.torso = load_sprite(RIG / "torso.png")
        self.head = load_sprite(RIG / "head.png")
        self.bucket = load_sprite(RIG / "bucket.png")
        self.tooth = load_sprite(RIG / "tooth.png")
        m = self.meta
        self.torso_o = np.array(m["torso"]["origin"], float)
        self.head_o = np.array(m["head"]["origin"], float)
        self.bucket_o = np.array(m["bucket"]["origin"], float)
        self.tooth_o = np.array(m["mouth"]["tooth_origin"], float) - self.head_o
        hh, hw = self.head.shape[:2]
        self.hw, self.hh = hw, hh
        self._build_warp_fields()
        # Augenparameter in Kopf-Koordinaten
        eL, eR = m["eyes"]
        self.eL = dict(c=np.array(eL["center"]) - self.head_o, h=np.array(eL["half"]) + 1.5,
                       iris_r=58.0, pupil_r=27.0, base_look=np.array(eL["iris_center"]) - np.array(eL["center"]))
        self.eR = dict(c=np.array(eR["center"]) - self.head_o, h=np.array(eR["half"]) + 1.5,
                       iris_r=33.0, pupil_r=15.0, base_look=np.array(eR["iris_center"]) - np.array(eR["center"]))
        self.mouth_c = np.array([475.0, 893.0]) - self.head_o
        # Fell-Textur (Bauch) fuer die Lider, auf Kopf-Fellfarbe normiert
        tp = self.torso[150:310, 110:270, :3] / np.maximum(self.torso[150:310, 110:270, 3:4], 1e-3)
        tp = tp * 255.0
        tp = tp / np.maximum(tp.reshape(-1, 3).mean(0), 1.0) * np.array(FUR, np.float32)
        self.lid_tex = np.tile(np.clip(tp, 0, 255), (3, 3, 1)).astype(np.float32)

    # ------------------------------------------------------------------
    def _build_warp_fields(self):
        hh, hw = self.hh, self.hw
        yy, xx = np.mgrid[0:hh, 0:hw].astype(np.float32)
        ox, oy = self.meta["head"]["origin"]
        xs, ys = xx + ox, yy + oy                      # Referenz-Koordinaten
        # linkes Ohr: Anker am Kopf
        self.earL_c = (255.0 - ox, 690.0 - oy)
        wl = 1 - _smoothstep(120, 300, xs)
        wl *= _smoothstep(430, 560, ys) * (1 - _smoothstep(830, 930, ys))
        # rechtes Ohr
        self.earR_c = (705.0 - ox, 830.0 - oy)
        wr = _smoothstep(690, 830, xs) * _smoothstep(640, 760, ys) * (1 - _smoothstep(900, 960, ys))
        # Banane
        wb = np.clip((560.0 - ys) / 400.0, 0, 1) ** 1.4
        wb *= _smoothstep(440, 520, xs) * (1 - _smoothstep(740, 800, xs))
        self.wl, self.wr, self.wb = wl.astype(np.float32), wr.astype(np.float32), wb.astype(np.float32)
        self.xx, self.yy = xx, yy
        self.ban_h = np.clip((560.0 - ys) / 400.0, 0, 1).astype(np.float32)

    def _warped_head(self, earL, earR, ban):
        if abs(earL) < 0.05 and abs(earR) < 0.05 and abs(ban) < 0.05:
            return self.head.copy()
        mx = self.xx.copy()
        my = self.yy.copy()
        for w, c, ang in ((self.wl, self.earL_c, earL), (self.wr, self.earR_c, earR)):
            if abs(ang) < 0.05:
                continue
            th = np.radians(-ang) * w
            cs, sn = np.cos(th), np.sin(th)
            dx, dy = self.xx - c[0], self.yy - c[1]
            mx += (cs - 1) * dx - sn * dy
            my += sn * dx + (cs - 1) * dy
        if abs(ban) >= 0.05:
            mx -= ban * 2.5 * self.wb
        return cv2.remap(self.head, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT,
                         borderValue=(0, 0, 0, 0))

    # ------------------------------------------------------------------
    def _eye_layer(self, e, p, side):
        """Ein Auge prozedural. Rueckgabe: (premul float BGRA, origin_x, origin_y) in Kopf-Koordinaten."""
        esc = p["escL"] if side == "L" else p["escR"]
        hx, hy = e["h"][0] * esc, e["h"][1] * esc
        pad = 26
        w, h = int(2 * hx + 2 * pad), int(2 * hy + 2 * pad)
        cx, cy = w / 2.0, h / 2.0
        ox, oy = e["c"][0] - cx, e["c"][1] - cy
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        nx, ny = (xx - cx) / hx, (yy - cy) / hy
        r = np.hypot(nx, ny)

        img = np.zeros((h, w, 3), np.float32)
        # Augapfel: Kugel-Shading, Licht von links oben
        shade = 0.5 + 0.5 * np.clip(-(nx * 0.55 + ny * 0.6), -1, 1)      # 1 = hell
        white = np.array([196, 208, 222], np.float32) + shade[..., None] * np.array([36, 26, 14], np.float32)
        ao = np.clip((r - 0.72) / 0.28, 0, 1)[..., None] ** 1.6
        white = white * (1 - 0.42 * ao) + np.array(FUR_DARK, np.float32) * 0.42 * ao
        img[:] = white
        mask = np.zeros((h, w), np.uint8)
        cv2.ellipse(mask, (int(round(cx * 16)), int(round(cy * 16))), (int(hx * 16), int(hy * 16)), 0, 0, 360, 255, -1,
                    cv2.LINE_AA, 4)
        eye_mask = mask.astype(np.float32) / 255.0

        # Blick
        if side == "R" and p["lookRx"] is not None:
            lx, ly = p["lookRx"], p["lookRy"]
        else:
            lx, ly = p["lookx"], p["looky"]
        ir = e["iris_r"] * esc * (0.94 + 0.06 * p["pup"])
        rx = max(hx - ir * 0.72, 4)
        ry = max(hy - ir * 0.72, 4)
        icx, icy = cx + lx * rx, cy + ly * ry
        d = np.hypot(xx - icx, yy - icy)
        t = np.clip(d / ir, 0, 1)
        iris = np.zeros((h, w, 3), np.float32)
        # Iris-Verlauf: aussen dunkles Braun, innen warmes Braun
        c_out = np.array([28, 42, 68], np.float32)
        c_mid = np.array([44, 78, 128], np.float32)
        c_in = np.array([70, 128, 190], np.float32)
        kk = t[..., None]
        iris = np.where(kk < 0.55, c_in * (1 - kk / 0.55) + c_mid * (kk / 0.55),
                        c_mid * (1 - (kk - 0.55) / 0.45) + c_out * ((kk - 0.55) / 0.45))
        pr = e["pupil_r"] * esc * p["pup"]
        pupil = np.clip((pr - d) / 2.0 + 0.5, 0, 1)[..., None]
        iris = iris * (1 - pupil) + np.array([12, 10, 14], np.float32) * pupil
        # Glanzlichter
        for (hxo, hyo, hr, k) in ((0.34, -0.36, 0.20, 1.0), (-0.28, 0.32, 0.09, 0.7)):
            dd = np.hypot(xx - (icx + hxo * ir), yy - (icy + hyo * ir))
            hl = np.clip((hr * ir - dd) / 1.6 + 0.5, 0, 1)[..., None] * k
            iris = iris * (1 - hl) + np.array([255, 255, 255], np.float32) * hl
        iris_a = np.clip((ir - d) / 1.5 + 0.5, 0, 1)
        # weicher Schatten des Oberlids auf dem Augapfel
        img = img * (1 - iris_a[..., None]) + iris * iris_a[..., None]
        top_shadow = np.clip(1 - (ny + 1) / 0.55, 0, 1)[..., None]
        img *= (1 - 0.28 * top_shadow)

        # Lider
        lid_col = np.array(LID_BLUE if side == "R" else FUR, np.float32)
        crease = np.array((40, 50, 95) if side == "L" else (120, 50, 15), np.float32)
        lid_top = clamp(max(p["lidL" if side == "L" else "lidR"], p["blink"]))
        lid_low = clamp(p["lowL" if side == "L" else "lowR"])
        slant = p["slant"] * (1 if side == "L" else -1)          # innen = zur Nase hin
        # Nase liegt bei Kopf-x ~470: links ist innen = rechts
        inner_sign = 1 if side == "L" else -1
        alpha_lid = np.zeros((h, w), np.float32)
        edge_line = np.zeros((h, w), np.float32)
        if lid_top > 0.01:
            y_edge = cy - hy + lid_top * 2 * hy
            ang = math.radians(slant)
            # Linie durch (cx, y_edge), Neigung: innen tiefer
            line_y = y_edge + math.tan(ang) * (nx * hx) * inner_sign
            line_y = np.where(r < 1.0, line_y, y_edge)
            dist = yy - line_y
            alpha_lid = np.clip(-dist / 1.4 + 0.5, 0, 1)
            edge_line = np.clip(1 - np.abs(dist) / 3.2, 0, 1)
        alpha_low = np.zeros((h, w), np.float32)
        if lid_low > 0.01:
            y_edge = cy + hy - lid_low * 2 * hy
            dist = y_edge - yy
            alpha_low = np.clip(-dist / 1.4 + 0.5, 0, 1)
        lid_all = np.maximum(alpha_lid, alpha_low)
        lid_shade = 0.86 + 0.14 * np.clip((yy - (cy - hy)) / (2 * hy), 0, 1)
        if side == "R":
            lid_rgb = lid_col[None, None, :] * lid_shade[..., None]
            img = img * (1 - lid_all[..., None]) + lid_rgb * lid_all[..., None]
        line_a = edge_line * np.clip(1.25 - r, 0, 1) * (lid_top > 0.01)
        img = img * (1 - 0.45 * line_a[..., None]) + crease * 0.45 * line_a[..., None]

        # etwas groesser als das Auge, damit Lid-Farbe den inpainted Hintergrund ueberdeckt
        if side == "L":
            # Lid = Transparenz: darunter liegt sauber gefuelltes Kopffell
            a = np.clip(eye_mask * (1 - lid_all), 0, 1)
            shadow_a = np.clip(edge_line * np.clip(1.15 - r, 0, 1) * 0.40 * (lid_top > 0.01), 0, 1)
            img = img * (1 - shadow_a[..., None]) + crease * shadow_a[..., None]
            a = np.maximum(a, shadow_a * (1 - eye_mask * 0) * (lid_all > 0.5))
        else:
            cover = np.clip(1.06 - r * 0.0 - (r - 1.0) * 6.0, 0, 1)
            a = np.clip(cover, 0, 1)
        out = np.dstack([img / 255.0, a]).astype(np.float32)
        out[..., :3] *= out[..., 3:4]
        return out, ox, oy

    def _mouth_layer(self, p):
        w, h = 260, 200
        cx, cy = w / 2.0, 60.0
        img = np.zeros((h, w, 3), np.uint8)
        mk = np.zeros((h, w), np.uint8)
        o = clamp(p["mo"])
        smile = clamp(p["msm"], -1, 1)
        wide = clamp(p["mw"])
        hw_ = 42 + 34 * wide + 12 * o
        hh_ = 2.5 + 62 * o
        n = 40
        us = np.linspace(-1, 1, n)
        top = [(cx + u * hw_, cy - smile * 20 * u * u + 2) for u in us]
        bot = [(cx + u * hw_, cy - smile * 20 * u * u + 2 + hh_ * 2 * (1 - u * u) ** 0.75 + 3 * (1 - u * u)) for u in us]
        poly = top + bot[::-1]
        cv_col = (34, 26, 70)
        aa = lambda pts: np.array([(int(px * 16), int(py * 16)) for px, py in pts], np.int32)
        cv2.fillPoly(img, [aa(poly)], cv_col, cv2.LINE_AA, 4)
        cv2.fillPoly(mk, [aa(poly)], 255, cv2.LINE_AA, 4)
        if p["tongue"] > 0.02 or o > 0.35:
            tk = max(p["tongue"], 0.6 * clamp((o - 0.3) / 0.5))
            cyt = cy + hh_ * 1.55 + 2
            tmp = np.zeros((h, w), np.uint8)
            cv2.ellipse(tmp, (int(cx * 16), int(cyt * 16)), (int(hw_ * 0.62 * 16), int(hh_ * 0.62 * 16)), 0, 0, 360, 255, -1,
                        cv2.LINE_AA, 4)
            inside = cv2.bitwise_and(tmp, mk).astype(np.float32)[..., None] / 255.0 * tk
            img = (img * (1 - inside) + np.array((110, 96, 220), np.float32) * inside).astype(np.uint8)
        # Lippenlinie
        lip = (36, 40, 84)
        cv2.polylines(img, [aa(top)], False, lip, 4, cv2.LINE_AA, 4)
        cv2.polylines(mk, [aa(top)], False, 255, 4, cv2.LINE_AA, 4)
        if o < 0.18:
            cv2.polylines(img, [aa(bot)], False, lip, 3, cv2.LINE_AA, 4)
            cv2.polylines(mk, [aa(bot)], False, 255, 3, cv2.LINE_AA, 4)
        else:
            cv2.polylines(img, [aa(bot)], False, lip, 3, cv2.LINE_AA, 4)
            cv2.polylines(mk, [aa(bot)], False, 255, 3, cv2.LINE_AA, 4)
        out = np.dstack([img.astype(np.float32) / 255.0, mk.astype(np.float32) / 255.0])
        out[..., :3] *= out[..., 3:4]
        return out, self.mouth_c[0] - cx, self.mouth_c[1] - cy

    # ------------------------------------------------------------------
    @staticmethod
    def _over(dst, src, ox, oy):
        """src (premul float) an Position (ox,oy) ueber dst (premul float) legen."""
        ox, oy = int(round(ox)), int(round(oy))
        sh, sw = src.shape[:2]
        dh, dw = dst.shape[:2]
        x0, y0 = max(0, ox), max(0, oy)
        x1, y1 = min(dw, ox + sw), min(dh, oy + sh)
        if x1 <= x0 or y1 <= y0:
            return
        s = src[y0 - oy:y1 - oy, x0 - ox:x1 - ox]
        d = dst[y0:y1, x0:x1]
        d[:] = s + d * (1 - s[..., 3:4])

    def draw(self, canvas, cam, pose):
        p = dict(DEFAULT)
        p.update(pose)

        base = (Tm(p["x"], p["y"]) @ Rm(p["rot"]) @ Sm(p["s"] * p["sx"], p["s"] * p["sy"]) @ Tm(-FEET[0], -FEET[1]))
        C = cam.M
        Mb = C @ base
        # Torso mit eigenem Squash (um die Fuesse)
        Mt = Mb @ about(Sm(p["tsx"], p["tsy"]), FEET[0], FEET[1])

        soot = clamp(p["soot"])
        tint = (28, 30, 40, 0.55 * soot) if soot > 0 else None
        blit(canvas, self.torso, Mt @ Tm(*self.torso_o), opacity=p["opacity"], tint=tint)

        # Kopf
        head = self._warped_head(p["earL"], p["earR"], p["ban"])
        if soot > 0:
            head[..., :3] = head[..., :3] * (1 - 0.55 * soot) + np.array([28, 30, 40], np.float32) / 255.0 * 0.55 * soot * head[..., 3:4]
        for side, e in (("L", self.eL), ("R", self.eR)):
            lay, ox, oy = self._eye_layer(e, p, side)
            self._over(head, lay, ox, oy)
        lay, ox, oy = self._mouth_layer(p)
        self._over(head, lay, ox, oy)
        self._over(head, self.tooth, self.tooth_o[0], self.tooth_o[1] + 2 - 6 * clamp(p["mo"]) * 0.0)

        Mh = Mt @ Tm(NECK[0] + p["hdx"], NECK[1] + p["hdy"]) @ Rm(p["hrot"]) @ Sm(p["hsx"], p["hsy"]) @ Tm(-NECK[0], -NECK[1])
        blit(canvas, head, Mh @ Tm(*self.head_o), opacity=p["opacity"],
             tint=(255, 255, 255, p["flash"]) if p["flash"] > 0 else None)

        if p["pre_bucket"] is not None:
            p["pre_bucket"](canvas)
        if p["bucket"]:
            if p["bucketM"] is not None:
                Mk = C @ p["bucketM"]
            else:
                Mk = Mt @ about(Tm(p["bx"], p["by"]) @ Rm(p["brot"]) @ Sm(p["bs"]), 747.0, 1010.0)
            blit(canvas, self.bucket, Mk @ Tm(*self.bucket_o), opacity=p["opacity"])

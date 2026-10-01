"""Kleine deterministische 2D-Engine: Easing, Transformationen, Kamera, Blitting, FX.

Alles ist eine reine Funktion der Zeit t - damit kann jedes Frame unabhaengig
(und parallel) gerendert werden.
"""
import math
from functools import lru_cache
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FPS = 30


# ----------------------------------------------------------------------------
# Easing / Kurven
# ----------------------------------------------------------------------------
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def lerp(a, b, t):
    return a + (b - a) * t


def smooth(t):
    t = clamp(t)
    return t * t * (3 - 2 * t)


def e_out(t, p=3):
    t = clamp(t)
    return 1 - (1 - t) ** p


def e_in(t, p=3):
    t = clamp(t)
    return t ** p


def e_inout(t):
    t = clamp(t)
    return 4 * t * t * t if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2


def e_back(t, s=1.9):
    t = clamp(t)
    c3 = s + 1
    return 1 + c3 * (t - 1) ** 3 + s * (t - 1) ** 2


def e_elastic(t, amp=1.0, period=0.35):
    t = clamp(t)
    if t in (0.0, 1.0):
        return t
    return amp * 2 ** (-10 * t) * math.sin((t - period / 4) * 2 * math.pi / period) + 1


def spring(t, f=7.0, d=7.0):
    """Sprungantwort 0 -> 1 mit Ueberschwingen (t in Sekunden seit Ausloesung)."""
    if t <= 0:
        return 0.0
    return 1 - math.exp(-d * t) * math.cos(2 * math.pi * f * t)


def ring(t, f=9.0, d=6.0):
    """Abklingende Schwingung um 0 (Nachschwingen von Ohren, Banane ...)."""
    if t <= 0:
        return 0.0
    return math.exp(-d * t) * math.sin(2 * math.pi * f * t)


EASES = {"lin": lambda x: x, "out": e_out, "in": e_in, "io": e_inout, "back": e_back,
         "smooth": smooth, "step": lambda x: 1.0 if x >= 1 else 0.0, "elastic": e_elastic,
         "out2": lambda x: e_out(x, 2), "out5": lambda x: e_out(x, 5), "in2": lambda x: e_in(x, 2)}


def kf(t, keys, default_ease="io"):
    """Keyframes: [(zeit, wert, ease?), ...]. Ease gehoert zum Segment, das an diesem Key ENDET."""
    if t <= keys[0][0]:
        return keys[0][1]
    for i in range(1, len(keys)):
        t1 = keys[i][0]
        if t <= t1:
            t0, v0 = keys[i - 1][0], keys[i - 1][1]
            ease = keys[i][2] if len(keys[i]) > 2 else default_ease
            u = (t - t0) / max(t1 - t0, 1e-6)
            u = EASES[ease](clamp(u))
            v1 = keys[i][1]
            if isinstance(v0, (tuple, list)):
                return tuple(lerp(a, b, u) for a, b in zip(v0, v1))
            return lerp(v0, v1, u)
    return keys[-1][1]


def _hash(n):
    n = (n << 13) ^ n
    return 1.0 - ((n * (n * n * 15731 + 789221) + 1376312589) & 0x7FFFFFFF) / 1073741824.0


def noise1(seed, t, freq=1.0):
    """Glattes 1D-Rauschen in [-1, 1]."""
    x = t * freq
    i = math.floor(x)
    f = x - i
    a, b = _hash(int(i) * 57 + seed * 131), _hash(int(i + 1) * 57 + seed * 131)
    f = f * f * (3 - 2 * f)
    return a + (b - a) * f


def shake(t, amp, freq=28.0, seed=1):
    return amp * noise1(seed, t, freq), amp * noise1(seed + 17, t, freq)


def rng(seed):
    return np.random.default_rng(seed)


# ----------------------------------------------------------------------------
# 3x3-Transformationen
# ----------------------------------------------------------------------------
def Tm(x, y):
    m = np.eye(3)
    m[0, 2], m[1, 2] = x, y
    return m


def Sm(sx, sy=None):
    sy = sx if sy is None else sy
    m = np.eye(3)
    m[0, 0], m[1, 1] = sx, sy
    return m


def Rm(deg):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1.0]])


def about(M, px, py):
    """M um den Punkt (px,py) anwenden."""
    return Tm(px, py) @ M @ Tm(-px, -py)


class Cam:
    """Weltkamera: Zentrum, Zoom, Roll, Shake."""

    def __init__(self, cx=W / 2, cy=H / 2, z=1.0, roll=0.0, dx=0.0, dy=0.0):
        self.cx, self.cy, self.z, self.roll, self.dx, self.dy = cx, cy, z, roll, dx, dy
        self.M = Tm(W / 2 + dx, H / 2 + dy) @ Rm(roll) @ Sm(z) @ Tm(-cx, -cy)

    def pt(self, x, y):
        v = self.M @ np.array([x, y, 1.0])
        return float(v[0]), float(v[1])


# ----------------------------------------------------------------------------
# Sprites / Blitting (uint8-Canvas, Sprites als float32 premultiplied BGRA)
# ----------------------------------------------------------------------------
def premul(a):
    out = a.copy()
    out[..., :3] *= out[..., 3:4]
    return out


def load_sprite(path, scale=1.0):
    a = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if a.shape[2] == 3:
        a = np.dstack([a, np.full(a.shape[:2], 255, np.uint8)])
    a = a.astype(np.float32) / 255.0
    if scale != 1.0:
        a = cv2.resize(a, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    return premul(a)


def sprite_from_uint8_bgra(a):
    return premul(a.astype(np.float32) / 255.0)


def blit(canvas, spr, M, opacity=1.0, additive=False, tint=None):
    """Sprite (float premul BGRA) mit 3x3-Matrix M (Sprite-Pixel -> Bildschirm) auf uint8-Canvas."""
    h, w = spr.shape[:2]
    corners = np.array([[0, 0, 1], [w, 0, 1], [w, h, 1], [0, h, 1]], np.float64).T
    sc = M @ corners
    x0 = int(max(0, math.floor(sc[0].min()) - 1))
    y0 = int(max(0, math.floor(sc[1].min()) - 1))
    x1 = int(min(W, math.ceil(sc[0].max()) + 1))
    y1 = int(min(H, math.ceil(sc[1].max()) + 1))
    if x1 <= x0 or y1 <= y0:
        return
    M2 = Tm(-x0, -y0) @ M
    warped = cv2.warpAffine(spr, M2[:2], (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR,
                            borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    _composite(canvas, warped, x0, y0, opacity, additive, tint)


def _composite(canvas, warped, x0, y0, opacity, additive, tint):
    h, w = warped.shape[:2]
    roi = canvas[y0:y0 + h, x0:x0 + w].astype(np.float32)
    rgb = warped[..., :3]
    a = warped[..., 3:4]
    if tint is not None:          # tint = (b,g,r, amount) mischt Farbe ueber das Sprite
        tb, tg, tr, k = tint
        rgb = rgb * (1 - k) + np.array([tb, tg, tr], np.float32) / 255.0 * a * k
    if additive:
        roi += rgb * 255.0 * opacity
    else:
        roi = rgb * 255.0 * opacity + roi * (1.0 - a * opacity)
    canvas[y0:y0 + h, x0:x0 + w] = np.clip(roi, 0, 255).astype(np.uint8)


def blend_layer(canvas, layer_bgra_u8, x0=0, y0=0, opacity=1.0, additive=False):
    """uint8-BGRA-Layer (nicht premultiplied) an Position auf Canvas legen."""
    h, w = layer_bgra_u8.shape[:2]
    xa, ya = max(0, x0), max(0, y0)
    xb, yb = min(W, x0 + w), min(H, y0 + h)
    if xb <= xa or yb <= ya:
        return
    sub = layer_bgra_u8[ya - y0:yb - y0, xa - x0:xb - x0].astype(np.float32) / 255.0
    roi = canvas[ya:yb, xa:xb].astype(np.float32)
    a = sub[..., 3:4] * opacity
    if additive:
        roi += sub[..., :3] * a * 255.0
    else:
        roi = sub[..., :3] * 255.0 * a + roi * (1 - a)
    canvas[ya:yb, xa:xb] = np.clip(roi, 0, 255).astype(np.uint8)


# ----------------------------------------------------------------------------
# Glow / radiale Verlaeufe
# ----------------------------------------------------------------------------
@lru_cache(maxsize=None)
def _radial(size=256, power=2.2):
    y, x = np.mgrid[0:size, 0:size].astype(np.float32)
    r = np.hypot(x - size / 2, y - size / 2) / (size / 2)
    return np.clip(1 - r, 0, 1) ** power


@lru_cache(maxsize=256)
def _glow_sprite(color_bgr, power):
    base = _radial(256, power)
    return np.dstack([base * color_bgr[0] / 255, base * color_bgr[1] / 255,
                      base * color_bgr[2] / 255, base]).astype(np.float32)


def glow(canvas, cx, cy, radius, color_bgr, strength=1.0, power=2.2, additive=True):
    """Weicher radialer Lichtfleck (Bildschirmkoordinaten)."""
    if radius < 1 or strength <= 0:
        return
    spr = _glow_sprite(tuple(color_bgr), power)
    s = 2 * radius / 256
    M = Tm(cx - radius, cy - radius) @ Sm(s)
    if additive:
        blit(canvas, spr, M, opacity=strength, additive=True)
    else:
        blit(canvas, premul(spr), M, opacity=strength)


def vignette(canvas, strength=0.5, power=2.0):
    y, x = np.mgrid[0:H:8, 0:W:8].astype(np.float32)
    r = np.hypot((x - W / 2) / (W / 2), (y - H / 2) / (H / 2)) / 1.25
    v = 1 - strength * np.clip(r, 0, 1) ** power
    v = cv2.resize(v, (W, H), interpolation=cv2.INTER_LINEAR)
    canvas[:] = np.clip(canvas.astype(np.float32) * v[..., None], 0, 255).astype(np.uint8)


# ----------------------------------------------------------------------------
# Text
# ----------------------------------------------------------------------------
FONT_DIR = Path("C:/Windows/Fonts")


def font(name, size):
    for n in (name, "arialbd.ttf", "arial.ttf"):
        p = FONT_DIR / n
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


@lru_cache(maxsize=512)
def text_sprite(text, size, fill=(255, 255, 255), stroke=0, stroke_fill=(0, 0, 0), fontname="impact.ttf"):
    f = font(fontname, size)
    tmp = Image.new("RGBA", (10, 10))
    d = ImageDraw.Draw(tmp)
    box = d.textbbox((0, 0), text, font=f, stroke_width=stroke)
    w, h = box[2] - box[0] + 8, box[3] - box[1] + 8
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.text((4 - box[0], 4 - box[1]), text, font=f, fill=tuple(fill) + (255,), stroke_width=stroke,
           stroke_fill=tuple(stroke_fill) + (255,))
    a = np.asarray(img)[..., [2, 1, 0, 3]]   # RGBA -> BGRA
    return sprite_from_uint8_bgra(a)


# ----------------------------------------------------------------------------
# Zeichenhilfen mit Anti-Aliasing (auf uint8-BGR)
# ----------------------------------------------------------------------------
SH = 4
K = 1 << SH


def _p(x, y):
    return int(round(x * K)), int(round(y * K))


def aa_line(img, p0, p1, color, thick=2):
    cv2.line(img, _p(*p0), _p(*p1), color, max(1, int(round(thick))), cv2.LINE_AA, SH)


def aa_poly(img, pts, color):
    cv2.fillPoly(img, [np.array([_p(*p) for p in pts], np.int32)], color, cv2.LINE_AA, SH)


def aa_ellipse(img, c, axes, angle, color, thick=-1, start=0, end=360):
    cv2.ellipse(img, _p(*c), (int(round(axes[0] * K)), int(round(axes[1] * K))), angle, start, end, color,
                thick if thick < 0 else max(1, int(round(thick))), cv2.LINE_AA, SH)


def aa_polyline(img, pts, color, thick=2, closed=False):
    cv2.polylines(img, [np.array([_p(*p) for p in pts], np.int32)], closed, color, max(1, int(round(thick))),
                  cv2.LINE_AA, SH)


def overlay(canvas, draw_fn, opacity=1.0, additive=False, blur=0.0):
    """Zeichnet via draw_fn(img_bgr_u8, mask_u8) in temporaere Ebene und legt sie ueber den Canvas.
    draw_fn muss sowohl in img (Farbe) als auch in mask (255 = deckend) zeichnen."""
    img = np.zeros((H, W, 3), np.uint8)
    mask = np.zeros((H, W), np.uint8)
    draw_fn(img, mask)
    if blur > 0:
        img = cv2.GaussianBlur(img, (0, 0), blur)
        mask = cv2.GaussianBlur(mask, (0, 0), blur)
    a = (mask.astype(np.float32) / 255.0 * opacity)[..., None]
    if additive:
        canvas[:] = np.clip(canvas.astype(np.float32) + img.astype(np.float32) * opacity, 0, 255).astype(np.uint8)
    else:
        canvas[:] = np.clip(img.astype(np.float32) * a + canvas.astype(np.float32) * (1 - a), 0, 255).astype(np.uint8)

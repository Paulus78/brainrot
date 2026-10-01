"""Welt: Zimmer, Fenster mit Stadt, Handy, Lampe, Blitze und andere FX.

Alle Koordinaten sind Weltkoordinaten (1080x1920-Raum); Zeichnen laeuft ueber Cam.
"""
import math
from functools import lru_cache

import cv2
import numpy as np
from PIL import Image, ImageDraw

from engine import (W, H, Cam, Tm, Sm, Rm, about, blit, blend_layer, glow, clamp, lerp, rng, kf,
                    sprite_from_uint8_bgra, text_sprite, font, aa_line, aa_poly, aa_ellipse, aa_polyline, e_out)

SS = 1.5                       # Supersampling des statischen Hintergrunds
FLOOR_Y = 1290                 # Oberkante Sockelleiste unten = Wand/Boden-Grenze

WIN = (120, 250, 270, 520)      # Fenster: x, y, w, h (Welt)
PIC = (770, 330, 240, 300)     # Bilderrahmen
BULB = (600.0, 330.0)          # Gluehbirne Pendellampe

BGR = lambda r, g, b: (b, g, r)


# ============================================================================
# Statischer Hintergrund
# ============================================================================
def build_background():
    w, h = int(W * SS), int(H * SS)
    img = np.zeros((h, w, 3), np.float32)
    fy = int(FLOOR_Y * SS)

    ys = np.linspace(0, 1, fy)[:, None, None]
    top = np.array(BGR(38, 44, 96), np.float32)
    bot = np.array(BGR(86, 92, 168), np.float32)
    img[:fy] = top + (bot - top) * ys ** 1.2

    # feine Tapetenstreifen
    xs = np.arange(w)
    stripe = ((xs // int(60 * SS)) % 2).astype(np.float32)[None, :, None]
    img[:fy] *= (1.0 - 0.045 * stripe)

    # Boden
    fh = h - fy
    ys2 = np.linspace(0, 1, fh)[:, None, None]
    ft = np.array(BGR(74, 54, 92), np.float32)
    fb = np.array(BGR(30, 22, 44), np.float32)
    img[fy:] = ft + (fb - ft) * ys2 ** 0.8

    im8 = np.clip(img, 0, 255).astype(np.uint8)

    # Sockelleiste
    cv2.rectangle(im8, (0, fy - int(46 * SS)), (w, fy), BGR(30, 32, 72), -1)
    cv2.line(im8, (0, fy - int(46 * SS)), (w, fy - int(46 * SS)), BGR(96, 104, 190), int(3 * SS), cv2.LINE_AA)
    cv2.line(im8, (0, fy), (w, fy), BGR(14, 12, 30), int(4 * SS), cv2.LINE_AA)

    # Dielen (perspektivisch)
    vx, vy = w / 2, -900 * SS
    for i in range(-14, 15):
        x0 = w / 2 + i * 82 * SS
        x1 = w / 2 + i * 330 * SS
        cv2.line(im8, (int(x0), fy), (int(x1), h), BGR(22, 14, 34), int(2 * SS), cv2.LINE_AA)
    for k in range(1, 6):
        yy = fy + (h - fy) * (k / 6.0) ** 1.7
        cv2.line(im8, (0, int(yy)), (w, int(yy)), BGR(28, 18, 40), int(2 * SS), cv2.LINE_AA)

    # Fensterrahmen (Innenleben dynamisch)
    x, y, ww, wh = WIN
    fx0, fy0, fx1, fy1 = int(x * SS), int(y * SS), int((x + ww) * SS), int((y + wh) * SS)
    pad = int(16 * SS)
    cv2.rectangle(im8, (fx0 - pad, fy0 - pad), (fx1 + pad, fy1 + pad), BGR(228, 222, 236), -1)
    cv2.rectangle(im8, (fx0 - pad, fy0 - pad), (fx1 + pad, fy1 + pad), BGR(140, 132, 170), int(3 * SS), cv2.LINE_AA)
    cv2.rectangle(im8, (fx0, fy0), (fx1, fy1), BGR(8, 10, 24), -1)
    # Fensterbank
    cv2.rectangle(im8, (fx0 - pad - int(14 * SS), fy1 + pad), (fx1 + pad + int(14 * SS), fy1 + pad + int(22 * SS)),
                  BGR(238, 232, 244), -1)
    cv2.rectangle(im8, (fx0 - pad - int(14 * SS), fy1 + pad + int(22 * SS)),
                  (fx1 + pad + int(14 * SS), fy1 + pad + int(30 * SS)), BGR(60, 58, 110), -1)

    # weicher Boden-Schatten unter der Sockelleiste
    return im8


# ============================================================================
# Stadt (Fenster-Ausblick und Aussenshot)
# ============================================================================
class City:
    """Skyline in normierten Koordinaten [0,1]x[0,1]; Fenster gehen mit einer Welle aus."""

    def __init__(self, seed=7):
        r = rng(seed)
        self.layers = []
        # drei Ebenen: hinten (hell/klein) -> vorne (dunkel/gross)
        for li, (n, hmin, hmax, col) in enumerate([(22, 0.16, 0.38, BGR(34, 40, 92)),
                                                    (15, 0.20, 0.52, BGR(24, 28, 70)),
                                                    (9, 0.26, 0.66, BGR(14, 16, 44))]):
            bs = []
            x = -0.05
            while x < 1.05:
                bw = r.uniform(0.6, 1.3) / n
                bh = r.uniform(hmin, hmax)
                bs.append((x, bw, bh))
                x += bw * r.uniform(0.85, 1.05)
            wins = []
            for (bx, bw, bh) in bs:
                cols = max(2, int(bw * 46))
                rows = max(3, int(bh * 40))
                for cx in range(cols):
                    for cy in range(rows):
                        if r.random() < 0.55 - 0.12 * li:
                            wx = bx + bw * (0.12 + 0.76 * (cx + 0.5) / cols)
                            wy = 1.0 - bh + bh * (0.06 + 0.86 * (cy + 0.5) / rows)
                            warm = r.random()
                            wins.append((wx, wy, bw / cols * 0.42, bh / rows * 0.5, warm, r.random()))
            self.layers.append((col, bs, wins))
        self.stars = [(r.random(), r.random() * 0.5, r.random()) for _ in range(46)]
        self.src = (0.5, 0.86)     # Einschlagspunkt / Haus

    def draw(self, canvas, rect, blackout_t=None, t=0.0, speed=0.9, base_dark=0.0, depth_blur=False, relight_t=None):
        """rect=(x,y,w,h) in Bildschirmkoordinaten. blackout_t = Startzeit der Ausfall-Welle (None: nie)."""
        x, y, w, h = rect
        x0, y0 = int(max(0, x)), int(max(0, y))
        x1, y1 = int(min(W, x + w)), int(min(H, y + h))
        if x1 <= x0 or y1 <= y0:
            return
        sky = np.zeros((y1 - y0, x1 - x0, 3), np.float32)
        yy = (np.arange(y0, y1) - y) / h
        top = np.array(BGR(12, 14, 46), np.float32)
        hor = np.array(BGR(70, 44, 110), np.float32)
        sky[:] = (top + (hor - top) * np.clip(yy, 0, 1)[:, None, None] ** 1.5)
        sub = np.clip(sky * (1.0 - base_dark), 0, 255).astype(np.uint8)
        for (sx, sy, sb) in self.stars:
            px, py = int(x + sx * w) - x0, int(y + sy * h) - y0
            if 0 <= px < sub.shape[1] and 0 <= py < sub.shape[0]:
                cv2.circle(sub, (px, py), 1 if w < 600 else 2, (int(150 * sb + 80),) * 3, -1)
        glowl = np.zeros_like(sub)
        for li, (col, bs, wins) in enumerate(self.layers):
            for (bx, bw, bh) in bs:
                p0 = (int(x + bx * w) - x0, int(y + (1 - bh) * h) - y0)
                p1 = (int(x + (bx + bw) * w) - x0, int(y + h) - y0 + 2)
                cv2.rectangle(sub, p0, p1, col, -1)
            for (wx, wy, ww, wh, warm, rr) in wins:
                px, py = x + wx * w, y + wy * h
                # Ausfall-Zeit: Entfernung zum Einschlagspunkt
                lit = True
                flick = 1.0
                if blackout_t is not None:
                    d = math.hypot((wx - self.src[0]) * (w / h) * 1.0, (wy - self.src[1]))
                    off = blackout_t + d * speed * 1.7 + rr * 0.18
                    if t >= off:
                        lit = False
                    elif t > off - 0.16:
                        flick = 0.25 + 0.75 * (int((t - off) * 40) % 2)
                warm_c = None
                if not lit:
                    # nach dem Ausfall: einzelne Fenster gehen wieder an (Handy-Taschenlampen / Kerzen)
                    if relight_t is not None and rr > 0.80 and t > relight_t + (rr - 0.80) * 4.0:
                        lit = True
                        flick = 0.6 + 0.4 * (0.5 + 0.5 * math.sin(t * 17 + rr * 40))
                        warm_c = BGR(255, 190, 90) if warm > 0.5 else BGR(235, 245, 255)
                    else:
                        continue
                ww_, wh_ = max(1.0, ww * w), max(1.0, wh * h)
                c = warm_c if warm_c is not None else (BGR(255, 214, 120) if warm > 0.35 else BGR(190, 230, 255))
                c = tuple(int(v * flick) for v in c)
                cv2.rectangle(sub, (int(px - ww_ / 2) - x0, int(py - wh_ / 2) - y0),
                              (int(px + ww_ / 2) - x0, int(py + wh_ / 2) - y0), c, -1)
                if li == 0 or rr > 0.65:
                    cv2.rectangle(glowl, (int(px - ww_) - x0, int(py - wh_) - y0),
                                  (int(px + ww_) - x0, int(py + wh_) - y0), tuple(int(v * 0.5 * flick) for v in c), -1)
        if glowl.any():
            g = cv2.GaussianBlur(glowl, (0, 0), max(2.0, w / 120))
            sub = np.clip(sub.astype(np.int16) + g, 0, 255).astype(np.uint8)
        canvas[y0:y1, x0:x1] = sub


# ============================================================================
# Handy
# ============================================================================
PW, PH = 118, 236
PSC = 4


def _pfont(size):
    return font("arialbd.ttf", size)


@lru_cache(maxsize=400)
def phone_sprite(mode, pct=1, flash=0.0, extra=0.0, seed=0):
    """Handy als premultiplied BGRA, Groesse (PW*PSC, PH*PSC)."""
    S = PSC
    w, h = PW * S, PH * S
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=26 * S, fill=(96, 100, 112, 255))
    d.rounded_rectangle((3 * S, 3 * S, w - 3 * S, h - 3 * S), radius=24 * S, fill=(26, 28, 34, 255))
    sx0, sy0, sx1, sy1 = 8 * S, 9 * S, w - 8 * S, h - 9 * S
    sw, sh = sx1 - sx0, sy1 - sy0
    scr = Image.new("RGBA", (sw, sh), (0, 0, 0, 255))
    sd = ImageDraw.Draw(scr)

    def center_text(txt, cy, size, fill, stroke=0, stroke_fill=(0, 0, 0)):
        f = _pfont(size)
        bb = sd.textbbox((0, 0), txt, font=f, stroke_width=stroke)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        sd.text(((sw - tw) / 2 - bb[0], cy - th / 2 - bb[1]), txt, font=f, fill=fill, stroke_width=stroke,
                stroke_fill=stroke_fill)

    def battery(cx, cy, bw, bh, frac, col, outline=5):
        x0, y0 = cx - bw / 2, cy - bh / 2
        sd.rounded_rectangle((cx - bw * 0.2, y0 - bh * 0.07, cx + bw * 0.2, y0 + 2), radius=6, fill=col)
        sd.rounded_rectangle((x0, y0, x0 + bw, y0 + bh), radius=int(bw * 0.16), outline=col, width=outline * S // 2)
        if frac > 0:
            fh = max(6, (bh - 2 * outline * S / 2 - 8) * frac)
            sd.rounded_rectangle((x0 + outline * S / 2 + 4, y0 + bh - outline * S / 2 - 4 - fh,
                                  x0 + bw - outline * S / 2 - 4, y0 + bh - outline * S / 2 - 4), radius=6, fill=col)

    if mode in ("alert", "dying"):
        sd.rectangle((0, 0, sw, sh), fill=(20, 8, 12, 255))
        if flash > 0:
            sd.rectangle((0, 0, sw, sh), fill=(int(220 * flash + 20), 22, 34, 255))
        col = (255, 70, 70, 255) if flash < 0.6 else (255, 235, 235, 255)
        battery(sw / 2, sh * 0.30, sw * 0.5, sh * 0.28, 0.03 if mode == "alert" else 0.0, col)
        center_text("1%" if mode == "alert" else "0%", sh * 0.62, int(sw * 0.44), (255, 255, 255, 255))
        center_text("LOW BATTERY", sh * 0.82, int(sw * 0.09), (255, 210, 210, 255))
    elif mode == "charge":
        p = float(pct)
        if p > 999:
            hue = int(seed) % 180
            bgc = cv2.cvtColor(np.uint8([[[hue, 255, 255]]]), cv2.COLOR_HSV2RGB)[0, 0]
            sd.rectangle((0, 0, sw, sh), fill=(int(bgc[0]), int(bgc[1]), int(bgc[2]), 255))
        else:
            sd.rectangle((0, 0, sw, sh), fill=(10, 150, 66, 255))
            sd.rectangle((0, int(sh * 0.55), sw, sh), fill=(6, 110, 50, 255))
        # Blitz-Symbol
        bolt = [(0.56, 0.10), (0.34, 0.36), (0.50, 0.36), (0.42, 0.62), (0.68, 0.30), (0.52, 0.30)]
        sd.polygon([(sw * a, sh * b) for a, b in bolt], fill=(255, 240, 90, 255))
        txt = f"{int(p)}%"
        size = int(sw * (0.36 if len(txt) <= 3 else 0.27 if len(txt) == 4 else 0.22))
        center_text(txt, sh * 0.76, size, (255, 255, 255, 255), stroke=6, stroke_fill=(0, 60, 20))
    elif mode == "final":
        sd.rectangle((0, 0, sw, sh), fill=(16, 120, 210, 255))
        sd.rectangle((0, int(sh * 0.5), sw, sh), fill=(8, 84, 170, 255))
        battery(sw / 2, sh * 0.30, sw * 0.5, sh * 0.26, 1.0, (120, 255, 150, 255))
        center_text("100%", sh * 0.56, int(sw * 0.30), (255, 255, 255, 255))
        if extra > 0:
            k = clamp(extra)
            sd.rounded_rectangle((sw * 0.06, sh * (0.70 - 0.06 * (1 - k)), sw * 0.94, sh * (0.86 - 0.06 * (1 - k))),
                                 radius=22, fill=(235, 50, 60, 255))
            center_text("NO WI-FI", sh * (0.78 - 0.06 * (1 - k)), int(sw * 0.16), (255, 255, 255, 255))
    elif mode == "crt":
        u = clamp(extra)
        base = phone_sprite("dying", 0, 0.0, 0.0, 0)
        # Bildschirmbereich aus dem fertigen Sprite schneiden und vertikal kollabieren
        b8 = (base[..., [2, 1, 0, 3]] * 255).astype(np.uint8)
        b8[..., :3] = np.clip(b8[..., :3] / np.maximum(base[..., 3:4], 1e-3), 0, 255).astype(np.uint8)
        scr_crop = Image.fromarray(b8).crop((sx0, sy0, sx1, sy1))
        nh = max(3, int(sh * (1 - u) ** 2.2))
        nw = int(sw * (1 - max(0, u - 0.85) * 6.0)) if u > 0.85 else sw
        nw = max(4, nw)
        squeezed = scr_crop.resize((nw, nh))
        scr = Image.new("RGBA", (sw, sh), (0, 0, 0, 255))
        scr.paste(squeezed, ((sw - nw) // 2, (sh - nh) // 2))
        sd = ImageDraw.Draw(scr)
        sd.rectangle(((sw - nw) // 2, sh // 2 - 2, (sw + nw) // 2, sh // 2 + 2), fill=(255, 255, 255, 255))
    else:  # off
        sd.rectangle((0, 0, sw, sh), fill=(6, 7, 9, 255))
        sd.polygon([(sw * 0.15, 0), (sw * 0.45, 0), (sw * 0.05, sh * 0.5), (0, sh * 0.5), (0, sh * 0.2)],
                   fill=(255, 255, 255, 14))

    mask = Image.new("L", (sw, sh), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, sw - 1, sh - 1), radius=18 * S, fill=255)
    img.paste(scr, (sx0, sy0), mask)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((w * 0.36, sy0 + 5 * S, w * 0.64, sy0 + 14 * S), radius=5 * S, fill=(8, 8, 10, 255))
    d.ellipse((w * 0.62, sy0 + 6 * S, w * 0.62 + 7 * S, sy0 + 13 * S), fill=(30, 40, 70, 255))
    d.rounded_rectangle((w - 3 * S, h * 0.28, w + 1, h * 0.36), radius=S, fill=(120, 124, 136, 255))
    a = np.asarray(img)[..., [2, 1, 0, 3]]
    a = cv2.resize(a, (PW * 3, PH * 3), interpolation=cv2.INTER_AREA)
    return sprite_from_uint8_bgra(a)


PSPR = 3     # tatsaechlicher Sprite-Massstab (Pixel pro Welteinheit)


def draw_phone(canvas, cam, cx, cy, rot=0.0, sc=1.0, mode="off", pct=1, flash=0.0, extra=0.0, seed=0,
               opacity=1.0, tint=None):
    spr = phone_sprite(mode, int(pct), round(flash * 8) / 8.0, round(extra * 16) / 16.0, int(seed))
    h, w = spr.shape[:2]
    M = cam.M @ Tm(cx, cy) @ Rm(rot) @ Sm(sc / PSPR) @ Tm(-w / 2, -h / 2)
    blit(canvas, spr, M, opacity=opacity, tint=tint)


# ============================================================================
# Lampe, Rahmen
# ============================================================================
def draw_pendant(canvas, cam, on=1.0, sway=0.0, popped=False):
    bx, by = BULB
    ang = math.radians(sway)
    top = cam.pt(bx, -200)
    hang = 270.0
    tip = (bx + math.sin(ang) * hang, by - 70 + (1 - math.cos(ang)) * 0)
    p0 = cam.pt(bx, -200)
    p1 = cam.pt(*tip)
    aa_line(canvas, p0, p1, (20, 20, 26), max(2, 5 * cam.z))
    # Schirm
    sx, sy = tip
    shade = [(sx - 120, sy + 70), (sx - 50, sy - 30), (sx + 50, sy - 30), (sx + 120, sy + 70)]
    aa_poly(canvas, [cam.pt(*p) for p in shade], BGR(34, 38, 44))
    aa_poly(canvas, [cam.pt(sx - 120, sy + 70), cam.pt(sx + 120, sy + 70), cam.pt(sx + 112, sy + 62),
                     cam.pt(sx - 112, sy + 62)], BGR(90, 96, 104))
    if not popped:
        c = cam.pt(sx, sy + 96)
        aa_ellipse(canvas, c, (30 * cam.z, 34 * cam.z), 0, tuple(int(v) for v in (np.array(BGR(255, 236, 170)) * (0.4 + 0.6 * on))))
    else:
        c = cam.pt(sx, sy + 78)
        aa_ellipse(canvas, c, (14 * cam.z, 10 * cam.z), 0, BGR(60, 60, 70))
    return (sx, sy + 96)


@lru_cache(maxsize=4)
def _frame_sprite():
    x, y, w, h = PIC
    S = 2
    img = np.zeros((h * S, w * S, 4), np.uint8)
    cv2.rectangle(img, (0, 0), (w * S - 1, h * S - 1), BGR(206, 150, 46) + (255,), -1)
    cv2.rectangle(img, (12 * S, 12 * S), (w * S - 13 * S, h * S - 13 * S), BGR(250, 236, 206) + (255,), -1)
    # Gemaelde: der gelbe Smiley-Eimer (Bongos Schrein)
    cx, cy = w * S // 2, h * S // 2 + 6 * S
    bw_t, bw_b, bh = 62 * S, 50 * S, 84 * S
    body = np.array([(cx - bw_t, cy - bh // 2), (cx + bw_t, cy - bh // 2), (cx + bw_b, cy + bh // 2),
                     (cx - bw_b, cy + bh // 2)], np.int32)
    cv2.fillPoly(img, [body], BGR(245, 196, 20) + (255,), cv2.LINE_AA)
    cv2.polylines(img, [body], True, BGR(160, 110, 10) + (255,), 3 * S, cv2.LINE_AA)
    cv2.ellipse(img, (cx, cy - bh // 2), (bw_t, 10 * S), 0, 0, 360, BGR(255, 224, 90) + (255,), -1, cv2.LINE_AA)
    cv2.ellipse(img, (cx, cy - bh // 2 - 30 * S), (bw_t - 8 * S, 44 * S), 0, 200, 340, BGR(120, 120, 130) + (255,), 4 * S, cv2.LINE_AA)
    cv2.circle(img, (cx - 20 * S, cy - 8 * S), 6 * S, (20, 20, 20, 255), -1, cv2.LINE_AA)
    cv2.circle(img, (cx + 20 * S, cy - 8 * S), 6 * S, (20, 20, 20, 255), -1, cv2.LINE_AA)
    cv2.ellipse(img, (cx, cy + 4 * S), (28 * S, 20 * S), 0, 20, 160, (20, 20, 20, 255), 4 * S, cv2.LINE_AA)
    return sprite_from_uint8_bgra(img), S


def draw_frame(canvas, cam, tilt=0.0, dx=0.0, dy=0.0, opacity=1.0):
    spr, S = _frame_sprite()
    x, y, w, h = PIC
    M = cam.M @ Tm(x + w / 2 + dx, y + h / 2 + dy) @ Rm(tilt) @ Sm(1.0 / S) @ Tm(-w * S / 2, -h * S / 2)
    blit(canvas, spr, M, opacity=opacity)


# ============================================================================
# FX-Ebene (additiv)
# ============================================================================
class FX:
    def __init__(self):
        self.a = np.zeros((H, W, 3), np.uint8)
        self.used = False

    def line(self, p0, p1, color, thick=2):
        aa_line(self.a, p0, p1, color, thick)
        self.used = True

    def poly(self, pts, color):
        aa_poly(self.a, pts, color)
        self.used = True

    def circle(self, c, r, color, thick=-1):
        aa_ellipse(self.a, c, (r, r), 0, color, thick)
        self.used = True

    def apply(self, canvas, sigma=9.0, gain=1.0, glow_gain=1.1):
        if not self.used:
            return
        g = cv2.GaussianBlur(self.a, (0, 0), sigma)
        g2 = cv2.GaussianBlur(self.a, (0, 0), sigma * 3)
        out = canvas.astype(np.int16) + (self.a.astype(np.float32) * gain).astype(np.int16) \
            + (g.astype(np.float32) * glow_gain).astype(np.int16) + (g2.astype(np.float32) * 0.7).astype(np.int16)
        canvas[:] = np.clip(out, 0, 255).astype(np.uint8)


def bolt_points(p0, p1, seed, disp=0.14, levels=6):
    r = rng(seed)
    pts = [np.array(p0, float), np.array(p1, float)]
    d = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    amp = d * disp
    for _ in range(levels):
        new = [pts[0]]
        for i in range(len(pts) - 1):
            a, b = pts[i], pts[i + 1]
            mid = (a + b) / 2
            n = np.array([-(b - a)[1], (b - a)[0]])
            nn = np.linalg.norm(n)
            if nn > 0:
                mid = mid + n / nn * r.uniform(-amp, amp)
            new += [mid, b]
        pts = new
        amp *= 0.55
    return [tuple(p) for p in pts]


def draw_bolt(fx, p0, p1, seed, width=6.0, color=(255, 200, 120), core=(255, 255, 255), branches=2):
    pts = bolt_points(p0, p1, seed)
    fx.a  # noqa
    from engine import aa_polyline as _pl
    _pl(fx.a, pts, color, width * 2.2)
    _pl(fx.a, pts, core, max(1.5, width * 0.8))
    fx.used = True
    r = rng(seed + 99)
    for _ in range(branches):
        i = int(r.integers(len(pts) // 4, len(pts) * 3 // 4))
        a = np.array(pts[i])
        ang = r.uniform(-1.2, 1.2)
        d = np.array(p1) - np.array(p0)
        d = d / (np.linalg.norm(d) + 1e-6)
        rot = np.array([[math.cos(ang), -math.sin(ang)], [math.sin(ang), math.cos(ang)]]) @ d
        end = a + rot * r.uniform(0.15, 0.35) * math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        bp = bolt_points(tuple(a), tuple(end), seed + int(r.integers(1000)), levels=4)
        _pl(fx.a, bp, color, width * 1.2)
        _pl(fx.a, bp, core, max(1.0, width * 0.45))


def sparks(fx, cam, origin, tt, seed, n=24, speed=520.0, life=0.7, color=(120, 210, 255), gravity=900.0,
           spread=(0, 360), size=3.0):
    """Ballistische Funken, deterministisch aus tt (Sekunden seit Ausloesung)."""
    if tt < 0 or tt > life:
        return
    r = rng(seed)
    for i in range(n):
        ang = math.radians(r.uniform(*spread))
        sp = speed * r.uniform(0.35, 1.0)
        l = life * r.uniform(0.5, 1.0)
        if tt > l:
            continue
        vx, vy = math.cos(ang) * sp, math.sin(ang) * sp
        x = origin[0] + vx * tt
        y = origin[1] + vy * tt + 0.5 * gravity * tt * tt
        vx2, vy2 = vx, vy + gravity * tt
        k = 1 - tt / l
        p0 = cam.pt(x, y)
        p1 = cam.pt(x - vx2 * 0.03, y - vy2 * 0.03)
        c = tuple(int(v * k) for v in color)
        fx.line(p0, p1, c, max(1.0, size * k * cam.z * 0.6))


def speed_lines(fx, center, t, seed, n=44, r0=260, r1=1500, color=(190, 190, 190), thick=5.0, strength=1.0, fps=15):
    """Radiale Speedlines um center (Bildschirmkoordinaten); Muster wechselt mit fps."""
    r = rng(seed + int(t * fps))
    for i in range(n):
        ang = r.uniform(0, 2 * math.pi)
        a0 = r.uniform(r0, r0 * 1.7)
        a1 = r.uniform(r1 * 0.55, r1)
        w = r.uniform(0.35, 1.0) * thick
        dx, dy = math.cos(ang), math.sin(ang)
        px, py = -dy, dx
        p0 = (center[0] + dx * a0, center[1] + dy * a0)
        p1 = (center[0] + dx * a1 + px * w * 3, center[1] + dy * a1 + py * w * 3)
        p2 = (center[0] + dx * a1 - px * w * 3, center[1] + dy * a1 - py * w * 3)
        c = tuple(int(v * strength) for v in color)
        fx.poly([p0, p1, p2], c)


def burst_star(fx, center, r_out, r_in, n, rot, color):
    pts = []
    for i in range(n * 2):
        a = rot + math.pi * i / n
        rr = r_out if i % 2 == 0 else r_in
        pts.append((center[0] + math.cos(a) * rr, center[1] + math.sin(a) * rr))
    fx.poly(pts, color)


def shock_ring(fx, center, radius, thick, color):
    from engine import aa_ellipse as _el
    _el(fx.a, center, (radius, radius), 0, color, max(1, int(thick)))
    fx.used = True

"""Choreografie des Shorts "Bongo 1%": Kamera, Bongo-Pose, Props, FX - alles Funktionen von t."""
import math

import cv2
import numpy as np

import bongo as B
import timeline as TL
import world as Wd
from engine import (W, H, Cam, Tm, Sm, Rm, about, blit, glow, clamp, lerp, kf, shake, spring, ring, rng, smooth,
                    e_out, e_in, e_back, text_sprite, _glow_sprite, noise1, aa_ellipse, blend_layer)

BX, BY, BS = 620.0, 1370.0, 0.70
HEAD_C = (BX, BY - (1411 - 770) * BS)                       # Kopfmitte (Welt)
RIM = (BX + (748 - 470) * BS, BY - (1411 - 1101) * BS)       # Eimerrand-Mitte (Welt)
FIST = (BX + (747 - 470) * BS, BY - (1411 - 1010) * BS)      # Faust am Buegel
BANANA_TOP = (BX + (610 - 470) * BS, BY - (1411 - 150) * BS)
PH_REST = (262.0, 1282.0)
ln = math.log

T = TL


class Ctx:
    def __init__(self):
        self.bongo = B.Bongo()
        self.bg = Wd.build_background()
        self.city = Wd.City()


# ============================================================================
# Kamera
# ============================================================================
CAM_KEYS = [
    (0.00, (262, 1282, ln(3.30))),
    (T.T_WHIP0, (262, 1282, ln(3.95)), "lin"),
    (T.T_WHIP1, (600, 960, ln(1.20)), "io"),
    (1.92, (610, 940, ln(1.30)), "lin"),
    (2.22, (750, 1080, ln(1.62)), "out"),
    (2.42, (750, 1080, ln(1.62)), "lin"),
    (2.56, (540, 1020, ln(1.04)), "io"),
    (2.94, (600, 1010, ln(1.08)), "lin"),
    (3.06, (790, 1100, ln(1.45)), "out"),
    (3.36, (650, 1050, ln(1.32)), "io"),
    (T.T_STOP, (650, 1050, ln(1.40)), "lin"),
    (T.T_POP - 0.04, (700, 1090, ln(1.52)), "in2"),
    (T.T_POP + 0.10, (620, 890, ln(1.06)), "out"),
    (T.T_WHITE0, (630, 900, ln(1.12)), "lin"),
    (T.T_DARK_ROOM, (650, 930, ln(1.36)), "lin"),
    (T.T_EXT2, (650, 930, ln(1.46)), "lin"),
]


def banga_amp(t):
    if t < T.T_BANGA0:
        return 0.0
    if t <= T.T_STOP:
        u = (t - T.T_BANGA0) / (T.T_STOP - T.T_BANGA0)
        return 0.32 + 0.68 * u ** 0.8
    return 1.0 * math.exp(-(t - T.T_STOP) * 48.0)


def _imp(t, t0, amp, decay, seed, freq=30.0):
    if t < t0:
        return 0.0, 0.0
    return shake(t, amp * math.exp(-(t - t0) * decay), freq, seed)


def camera(t):
    cx, cy, lz = kf(t, CAM_KEYS)
    z = math.exp(lz)
    dx = dy = 0.0
    roll = 0.0
    for (t0, amp, dec, sd) in ((T.T_PING1, 7, 16, 1), (T.T_PING2, 7, 16, 2), (T.T_WHIP1, 12, 13, 3),
                               (T.T_IDEA, 6, 14, 4), (T.V_BUCKETO, 10, 12, 5), (T.T_KICK, 8, 12, 6),
                               (T.T_LAND, 15, 13, 7), (T.T_POP, 30, 7, 8), (T.T_EXT, 24, 9, 9)):
        a, b = _imp(t, t0, amp, dec, sd)
        dx += a
        dy += b
    a = banga_amp(t)
    if a > 0:
        sx, sy = shake(t, 4 + 20 * a, 26, 21)
        dx += sx
        dy += sy
        roll += 1.3 * a * noise1(31, t, 18)
        z *= 1 + 0.025 * a * abs(math.sin(2 * math.pi * 10 * t))
    if T.T_POP + 0.1 < t < T.T_WHITE0:
        sx, sy = shake(t, 5 + 10 * (t - T.T_POP), 34, 41)
        dx += sx
        dy += sy
    return Cam(cx, cy, z, roll, dx, dy)


# ============================================================================
# Ausdruck, Blick, Mund
# ============================================================================
EXPR_KEYS = [
    (0.00, "shocked", 0.04),
    (1.58, "suspicious", 0.10),
    (1.98, "realization", 0.05),
    (2.16, "confident", 0.10),
    (3.00, "pleased", 0.06),
    (3.22, "intense", 0.06),
    (T.T_STOP + 0.02, "annoyed", 0.04),
    (T.T_POP, "shocked", 0.02),
    (T.T_DARK_ROOM - 0.4, "smug", 0.30),
    (T.T_BANNER + 0.05, "pleased", 0.12),
]


def expr_at(t):
    idx = 0
    for i, (t0, _, _) in enumerate(EXPR_KEYS):
        if t >= t0:
            idx = i
    t0, name, tr = EXPR_KEYS[idx]
    cur = B.EXPR[name]
    if idx == 0:
        return dict(cur)
    prev = B.EXPR[EXPR_KEYS[idx - 1][1]]
    k = smooth((t - t0) / tr)
    return B.mix_expr(prev, cur, k)


LOOK_KEYS = [
    (0.00, (-0.85, 0.75)),
    (1.40, (0.0, 0.05)),
    (T.T_LOOK_PHONE, (-0.90, 0.70)),
    (T.T_LOOK_BUCKET, (0.95, 0.75)),
    (2.12, (0.0, 0.0)),
    (T.T_LAND, (0.9, 0.8)),
    (3.14, (0.0, 0.05)),
    (T.T_STOP + 0.02, (0.9, 0.8)),
    (T.T_POP, (-0.25, -0.9)),
    (T.T_DARK_ROOM, (0.0, 0.10)),
    (T.T_BANNER - 0.05, (0.75, -0.5)),
    (T.T_BANNER + 0.16, (0.0, 0.10)),
]


def look_at(t):
    dart = 0.07
    idx = 0
    for i, (t0, _) in enumerate(LOOK_KEYS):
        if t >= t0:
            idx = i
    t0, v = LOOK_KEYS[idx]
    if idx == 0:
        return v
    pv = LOOK_KEYS[idx - 1][1]
    u = e_out((t - t0) / dart, 3)
    return (lerp(pv[0], v[0], u), lerp(pv[1], v[1], u))


def blink_amt(t):
    for tb in (1.30, 1.80, 2.86, 3.14, 6.98, 7.70, 8.24):
        d = t - tb
        if 0 <= d < 0.14:
            return 1 - abs(d / 0.07 - 1)
    return 0.0


# ============================================================================
# Handy-Zustand
# ============================================================================
def phone_state(t):
    """Gibt dict(cx,cy,rot,sc,mode,pct,flash,extra,seed,layer) oder None."""
    if t < T.T_KICK:
        st = dict(cx=PH_REST[0], cy=PH_REST[1], rot=-6.0, sc=1.0, mode="off", pct=1, flash=0.0, extra=0.0, seed=0,
                  layer="front")
        if t < T.T_DIE:
            f1 = math.exp(-(t - T.T_PING1) * 7.0) if t >= T.T_PING1 else 0.0
            f2 = math.exp(-(t - T.T_PING2) * 9.0) if t >= T.T_PING2 else 0.0
            st["flash"] = clamp(max(f1, f2) * 1.0 + 0.18)
            st["mode"] = "alert" if t < 0.56 else "dying"
            if t >= 0.56:
                st["flash"] = 0.55 * (int((t - 0.56) * 22) % 2)
            if (T.T_PING1 <= t < T.T_PING1 + 0.14) or (T.T_PING2 <= t < T.T_PING2 + 0.14):
                st["cx"] += 4 * math.sin(2 * math.pi * 45 * t)
        elif t < T.T_DIE + 0.10:
            st["mode"] = "crt"
            st["extra"] = (t - T.T_DIE) / 0.10
        return st
    if t < T.T_LAND:
        u = (t - T.T_KICK) / (T.T_LAND - T.T_KICK)
        ex = e_out(u, 1.0) if False else u
        x = lerp(PH_REST[0], RIM[0], smooth(u) * 0.35 + u * 0.65)
        y = lerp(PH_REST[1], RIM[1] - 40, u) - 470 * 4 * u * (1 - u)
        return dict(cx=x, cy=y, rot=-6 + 760 * u, sc=lerp(1.0, 0.72, u), mode="off", pct=1, flash=0.0, extra=0.0,
                    seed=0, layer="front" if u < 0.72 else "behind")
    if t < T.T_POP:
        return None
    tp = t - T.T_POP
    if t < T.T_DARK_ROOM:
        u = e_out(tp / 0.30, 3)
        hover = (690.0, 395.0)
        bob = 10 * math.sin(2 * math.pi * 1.6 * tp)
        x = lerp(RIM[0], hover[0], u) + (5 * math.sin(2 * math.pi * 33 * t) if tp > 0.3 else 0)
        y = lerp(RIM[1] - 30, hover[1], u) + (bob if tp > 0.3 else 0)
        pct = 100 * 10 ** (2.0 * clamp((tp - 0.05) / 0.66))
        pct = min(9999, pct)
        return dict(cx=x, cy=y, rot=lerp(0, -12, u) + 8 * math.sin(tp * 5), sc=lerp(0.8, 1.9, u), mode="charge",
                    pct=pct, flash=0.0, extra=0.0, seed=int(t * 30) * 7, layer="glow")
    # dunkler Raum: Handy schwebt, zeigt 100%
    q = t - T.T_DARK_ROOM
    return dict(cx=905.0, cy=610.0 + 9 * math.sin(2 * math.pi * 0.9 * q), rot=-9 + 3 * math.sin(q * 1.3), sc=1.30,
                mode="final", pct=100, flash=0.0,
                extra=e_back(clamp((t - T.T_BANNER) / 0.16)) if t >= T.T_BANNER else 0.0, seed=0, layer="glow")


# ============================================================================
# Bongo-Pose
# ============================================================================
def _land(t, t0, amp, f=4.0, d=8.0):
    """Landungs-Squash: amp bei t0, danach Ausschwingen."""
    if t < t0:
        return 0.0
    tt = t - t0
    return amp * math.exp(-d * tt) * math.cos(2 * math.pi * f * tt)


def bongo_pose(t, ph):
    p = dict(x=BX, y=BY, s=BS)
    p.update(expr_at(t))
    lx, ly = look_at(t)
    p["lookx"], p["looky"] = lx, ly
    p["blink"] = blink_amt(t)

    # ---- Handy-Verfolgung im Flug
    if ph is not None and T.T_KICK <= t < T.T_LAND:
        p["lookx"] = clamp((ph["cx"] - HEAD_C[0]) / 260.0, -1, 1)
        p["looky"] = clamp((ph["cy"] - HEAD_C[1]) / 220.0, -1, 1)

    sy = 1.0 + 0.010 * math.sin(2 * math.pi * 0.9 * t)
    sx = 1.0
    yoff = 0.0
    rot = 0.0
    hrot = hdx = hdy = 0.0
    earL = earR = ban = 0.0
    tsy = 1.0

    # ---- Schock-Sprung (Handy stirbt)
    tj = t - 0.66
    if 0 <= tj < 0.44:
        u = tj / 0.44
        yoff -= 78 * 4 * u * (1 - u)
        sy *= 1 + 0.10 * (1 - abs(2 * u - 1))
        sx *= 1 - 0.05 * (1 - abs(2 * u - 1))
        earL += -34 * (1 - abs(2 * u - 1))
        earR += 34 * (1 - abs(2 * u - 1))
        ban += 22 * (1 - abs(2 * u - 1))
    ls = _land(t, 1.10, 0.10, 4.5, 8.5)
    sy *= 1 - ls
    sx *= 1 + ls * 0.7
    earL += 26 * ring(t - 1.10, 8, 6)
    earR -= 26 * ring(t - 1.10, 8, 6)
    ban += 30 * ring(t - 1.10, 6, 5)

    # ---- "Bongo... no." Kopfschuetteln
    if T.V_NO <= t < T.V_NO + 0.56:
        u = (t - T.V_NO) / 0.56
        fade = 1 - u ** 2
        hrot += 9 * math.sin(2 * math.pi * 3.3 * (t - T.V_NO)) * fade
        hdx += 14 * math.sin(2 * math.pi * 3.3 * (t - T.V_NO) + 1.2) * fade
        sy *= 1 - 0.025 * TL.env_at("no", t)

    # ---- Verdacht -> Blick zum Eimer
    hrot += kf(t, [(1.56, 0), (1.70, -7, "out"), (1.90, -7, "lin"), (2.00, 9, "back"), (2.16, 0, "io")])
    rot += kf(t, [(1.56, 0), (1.70, -2.0, "out"), (1.90, -2.0, "lin"), (2.0, 2.5, "io"), (2.2, 0, "io")])

    # ---- Erkenntnis: Squat -> Hopser
    if 1.90 <= t < 1.98:
        u = (t - 1.90) / 0.08
        sy *= 1 - 0.07 * math.sin(u * math.pi / 2)
        sx *= 1 + 0.04 * u
    elif 1.98 <= t < 2.14:
        u = (t - 1.98) / 0.16
        yoff -= 30 * 4 * u * (1 - u)
        sy *= 1 + 0.07 * (1 - abs(2 * u - 1))
    ls = _land(t, 2.14, 0.06, 5.0, 10.0)
    sy *= 1 - ls
    earL += 18 * ring(t - 1.98, 9, 6)
    earR -= 18 * ring(t - 1.98, 9, 6)

    # ---- "Bongo... bucketo": stolz, Brust raus
    k = smooth((t - 2.14) / 0.10) * (1 - smooth((t - 2.9) / 0.15))
    tsy *= 1 + 0.035 * k
    hdy -= 9 * k
    hrot += -3 * k

    # ---- Kick
    if 2.30 <= t < 2.40:
        u = (t - 2.30) / 0.10
        rot += 6 * u
        sy *= 1 - 0.05 * u
        hrot += 5 * u
    elif 2.40 <= t < 2.66:
        u = (t - 2.40) / 0.26
        rot += lerp(-9, 0, e_out(u, 2)) if u > 0.0 else 0
        yoff -= 22 * 4 * u * (1 - u)
        hrot += lerp(-8, 0, u)
        earL += 20 * ring(t - 2.40, 8, 7)
        earR -= 20 * ring(t - 2.40, 8, 7)

    # ---- Landung im Eimer: kleiner Nicker
    if t >= T.T_LAND:
        hdy += 10 * ring(t - T.T_LAND, 5, 7)
        hrot += 5 * ring(t - T.T_LAND, 4, 6)

    # ---- BANGA BANGA
    a = banga_amp(t)
    tw = T.T_BANGA0 - 0.06
    if tw <= t < T.T_BANGA0:                       # Ausholen
        u = (t - tw) / 0.06
        rot += -6 * u
        sy *= 1 - 0.05 * u
    if a > 0:
        ph_ = 2 * math.pi * 10.0 * t
        yoff += -20 * a * abs(math.sin(ph_))
        p["x"] += 36 * a * math.sin(ph_)
        rot += 6.5 * a * math.sin(ph_ + 0.6)
        sy *= 1 - 0.075 * a * abs(math.cos(ph_))
        sx *= 1 + 0.04 * a * abs(math.cos(ph_))
        hrot += -12 * a * math.sin(ph_ - 0.9)
        hdx += 22 * a * math.sin(ph_ - 1.1)
        earL += 40 * a * math.sin(ph_ + 1.6)
        earR += a * (20 + 20 * math.sin(ph_ + 2.3))
        ban += 40 * a * math.sin(ph_ - 1.4)
        if t < T.T_STOP:
            p["lookx"] += 0.30 * math.sin(2 * math.pi * 8 * t)
            p["looky"] += 0.30 * math.cos(2 * math.pi * 9 * t)
            p["pup"] = 0.62 + 0.25 * math.sin(2 * math.pi * 10 * t)
        for nm in ("banga1", "banga2"):
            sy *= 1 + 0.045 * TL.env_at(nm, t)

    # ---- POP / Stromschlag
    tp = t - T.T_POP
    if 0 <= tp < (T.T_DARK_ROOM - T.T_POP):
        if tp < 0.7:
            rot += -10 * (1 - smooth(tp / 0.5)) * (1 if tp < 0.5 else 0)
            yoff -= 34 * math.exp(-tp * 9) * abs(math.cos(tp * 20))
        p["soot"] = clamp((tp - 0.10) / 0.5) * 0.62
        if t < T.T_WHITE0 + 0.05:
            p["hsx"] = 1.07 + 0.02 * math.sin(tp * 60)
            p["hsy"] = 1.07 + 0.02 * math.cos(tp * 55)
            hdx += 4 * math.sin(2 * math.pi * 30 * t)
            p["x"] += 3 * math.sin(2 * math.pi * 31 * t + 1)
            earL += -30 + 9 * math.sin(2 * math.pi * 17 * t)
            earR += 30 + 9 * math.sin(2 * math.pi * 19 * t)
            ban += 32 * math.sin(2 * math.pi * 21 * t)
            p["flash"] = 0.9 * math.exp(-tp * 20)
            p.update(mo=0.95, tongue=0.55, mw=0.4, msm=-0.15, pup=0.4)
    elif tp >= (T.T_DARK_ROOM - T.T_POP):
        p["soot"] = 0.62
        p["hsx"], p["hsy"] = 1.05, 1.04
        earL += -14 + 3 * math.sin(t * 2)
        earR += 14 + 3 * math.sin(t * 2.3)
        ban += 10 * math.sin(t * 2.2)

    # ---- Handy-Banner-Reaktion
    if t >= T.T_BANNER:
        hdy += 5 * ring(t - T.T_BANNER, 5, 8)

    # ---- Mund zur Stimme
    sp = TL.speaking(t)
    if sp is not None:
        e = TL.env_at(sp, t)
        base_mo = p.get("mo", 0.1)
        if sp in ("banga1", "banga2"):
            p["mo"] = clamp(0.30 + 0.70 * e)
            p["mw"] = 0.9
            p["msm"] = 0.1
        elif sp == "no":
            p["mo"] = clamp(0.16 + 0.84 * e)
            p["msm"] = -0.25
        else:
            p["mo"] = clamp(0.12 + 0.85 * e)
            p["msm"] = max(p.get("msm", 0), 0.6)
    elif T.T_BANGA0 < t < T.T_STOP:
        p.update(mo=0.42, mw=1.0, msm=0.0)

    p.update(y=BY + yoff + (p.get("y", BY) - BY), sy=sy, sx=sx, rot=rot + p.get("rot", 0), hrot=hrot, hdx=hdx,
             hdy=hdy, earL=earL, earR=earR, ban=ban, tsy=tsy)

    # ---- Eimer
    brot = 0.0
    bs = 1.0
    bx = by = 0.0
    # Pop (bucketo)
    if t >= 2.10:
        u = t - 2.10
        bs *= 1 + 0.30 * math.exp(-u * 9) * math.cos(2 * math.pi * 4.5 * u) * (1 if u < 0.6 else 0) * 1.0
        brot += -24 * math.exp(-u * 8) * math.cos(2 * math.pi * 3.5 * u) * (1 if u < 0.7 else 0)
    if t >= T.T_LAND:
        u = t - T.T_LAND
        bs *= 1 - 0.13 * math.exp(-u * 9) * math.cos(2 * math.pi * 6 * u)
        brot += 7 * ring(u, 7, 6)
    if a > 0:
        ph_ = 2 * math.pi * 10.0 * t
        brot += 38 * a * math.sin(ph_ + math.pi / 2)
        bs *= 1 + 0.07 * a * math.sin(2 * ph_)
        bx += 8 * a * math.sin(ph_ * 0.5)
    if T.T_STOP < t < T.T_POP:
        by += 1.5 * math.sin(2 * math.pi * 31 * t)
        bx += 1.5 * math.sin(2 * math.pi * 27 * t)
    if t >= T.T_POP:
        u = t - T.T_POP
        bs *= 1 + 0.22 * math.exp(-u * 7) * math.cos(2 * math.pi * 5 * u) - 0.12 * math.exp(-u * 40)
        brot += 8 * ring(u, 6, 5)
    p.update(brot=brot, bs=bs, bx=bx, by=by)
    return p


# ============================================================================
# kleine Zeichenhelfer
# ============================================================================
def shadow(canvas, cam, cx, cy, w, h, strength=0.5):
    spr = _glow_sprite((0, 0, 0), 1.1)
    spr = spr.copy()
    M = cam.M @ Tm(cx, cy) @ Sm(w / 256.0, h / 256.0) @ Tm(-128, -128)
    from engine import premul
    blit(canvas, premul(spr), M, opacity=strength)


def grade(canvas, dark, lights):
    if dark <= 0.001 and not lights:
        return
    hh, ww = H // 8, W // 8
    m = np.full((hh, ww, 3), 1.0 - dark, np.float32)
    yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32)
    for (sx, sy, rad, col, st) in lights:
        d = np.hypot(xx * 8 - sx, yy * 8 - sy) / max(rad, 1)
        k = np.clip(1 - d, 0, 1) ** 1.5 * st
        m += k[..., None] * (np.array(col, np.float32) / 255.0)
    m = np.clip(m, 0, 1.5)
    up = cv2.resize(m, (W, H), interpolation=cv2.INTER_LINEAR)
    canvas[:] = np.clip(canvas.astype(np.float32) * up, 0, 255).astype(np.uint8)


def motion_blur(canvas, vx, vy):
    n = int(min(90, math.hypot(vx, vy)))
    if n < 3:
        return
    k = np.zeros((n, n), np.float32)
    ang = math.atan2(vy, vx)
    c = (n - 1) / 2.0
    for i in range(n):
        k[int(round(c + math.sin(ang) * (i - c))), int(round(c + math.cos(ang) * (i - c)))] = 1
    k /= k.sum()
    canvas[:] = cv2.filter2D(canvas, -1, k, borderType=cv2.BORDER_REPLICATE)


def zoom_canvas(canvas, z, dx=0.0, dy=0.0, cx=W / 2, cy=H / 2):
    M = np.array([[z, 0, cx - z * cx + dx], [0, z, cy - z * cy + dy]], np.float32)
    canvas[:] = cv2.warpAffine(canvas, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


def overlay_white(canvas, a):
    if a <= 0:
        return
    canvas[:] = np.clip(canvas.astype(np.float32) * (1 - a) + 255.0 * a, 0, 255).astype(np.uint8)


# ============================================================================
# Raum
# ============================================================================
def room_frame(t, ctx):
    canvas = np.zeros((H, W, 3), np.uint8)
    cam = camera(t)
    z = cam.z

    # Hintergrund (Supersampling 1.5x)
    Mbg = cam.M @ Sm(1.0 / Wd.SS)
    canvas[:] = cv2.warpAffine(ctx.bg, Mbg[:2], (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

    # Fenster: Stadt
    wx, wy, ww, wh = Wd.WIN
    p0 = cam.pt(wx, wy)
    p1 = cam.pt(wx + ww, wy + wh)
    ctx.city.draw(canvas, (p0[0], p0[1], p1[0] - p0[0], p1[1] - p0[1]), blackout_t=T.T_BLACKOUT, t=t, speed=0.55)
    # Fensterkreuz
    fx_ = (p0[0] + p1[0]) / 2
    fy_ = (p0[1] + p1[1]) / 2
    cv2.line(canvas, (int(fx_), int(p0[1])), (int(fx_), int(p1[1])), (228, 222, 236), max(2, int(9 * z)), cv2.LINE_AA)
    cv2.line(canvas, (int(p0[0]), int(fy_)), (int(p1[0]), int(fy_)), (228, 222, 236), max(2, int(9 * z)), cv2.LINE_AA)

    # Tiefenunschaerfe bei starkem Zoom
    if z > 1.6:
        s = 2.0 + (z - 1.6) * 5.0
        canvas[:] = cv2.GaussianBlur(canvas, (0, 0), s)

    ph = phone_state(t)
    pop = t >= T.T_BULB
    on = 0.0 if pop else 1.0

    # Bilderrahmen
    fall = t - T.T_FRAME_FALL
    if fall < 0:
        Wd.draw_frame(canvas, cam)
    elif fall < 0.8:
        g = fall
        Wd.draw_frame(canvas, cam, tilt=-30 * min(1, g / 0.25) - 60 * g, dx=-30 * g, dy=900 * g * g + 20 * g,
                      opacity=1.0)

    # Lampe
    sway = 0.0
    if T.T_POP <= t < T.T_BULB:
        sway = 8 * math.sin(2 * math.pi * 6 * t)
    bulb_pos = Wd.draw_pendant(canvas, cam, on=on, sway=sway, popped=pop)

    # Schatten
    bp = None
    shadow(canvas, cam, BX, BY + 8, 600 * BS / 0.7 * 0.85, 60, 0.55)
    if ph is not None and ph["layer"] in ("front", "behind") and t < T.T_KICK + 0.02:
        shadow(canvas, cam, ph["cx"], PH_REST[1] + 121, 130, 26, 0.5)

    # Bongo
    pose = bongo_pose(t, ph)
    pre = None
    if ph is not None and ph["layer"] == "behind":
        def pre(c, ph=ph):
            Wd.draw_phone(c, cam, ph["cx"], ph["cy"], ph["rot"], ph["sc"], ph["mode"], ph["pct"], ph["flash"],
                          ph["extra"], ph["seed"])
    pose["pre_bucket"] = pre
    ctx.bongo.draw(canvas, cam, pose)

    # Handy (vorn)
    if ph is not None and ph["layer"] in ("front", "glow"):
        Wd.draw_phone(canvas, cam, ph["cx"], ph["cy"], ph["rot"], ph["sc"], ph["mode"], ph["pct"], ph["flash"],
                      ph["extra"], ph["seed"])

    # ---- Beleuchtung
    dark = 0.16
    lights = []
    if not pop:
        bs_ = cam.pt(*bulb_pos)
        lights.append((bs_[0], bs_[1], 1500 * z, (110, 190, 255), 0.55))
    else:
        d = smooth((t - T.T_BULB) / 0.06)
        dark = lerp(0.16, 0.86, d)
    if ph is not None and ph["layer"] == "glow":
        sc_ = cam.pt(ph["cx"], ph["cy"])
        if ph["mode"] == "charge":
            lights.append((sc_[0], sc_[1], 1500 * z, (200, 255, 230), 0.9 + 0.1 * math.sin(t * 60)))
        else:
            lights.append((sc_[0], sc_[1], 1500 * z, (255, 236, 200), 1.15))
    grade(canvas, dark, lights)
    if ph is not None and ph["mode"] in ("alert", "dying") and ph["flash"] > 0.02:
        pc = cam.pt(ph["cx"], ph["cy"])
        glow(canvas, pc[0], pc[1], 900 * z / 3.3 * 1.6, (40, 40, 255), 0.75 * ph["flash"])

    # ---- Glow + FX
    fx = Wd.FX()
    # Handy-Glow
    if ph is not None and ph["layer"] == "glow":
        sc_ = cam.pt(ph["cx"], ph["cy"])
        if ph["mode"] == "charge":
            k = clamp((ph["pct"] - 100) / 9900.0)
            glow(canvas, sc_[0], sc_[1], (260 + 700 * k) * z * ph["sc"] / 2.2, (190, 255, 170), 0.55 + 0.4 * k)
        else:
            glow(canvas, sc_[0], sc_[1], 380 * z, (255, 220, 150), 0.30)

    # Bucket-Glow beim Banga
    a = banga_amp(t)
    rim_s = None
    if T.T_BANGA0 - 0.05 < t < T.T_POP + 0.25:
        rim_s = cam.pt(RIM[0], RIM[1] - 20)
        if t < T.T_STOP + 0.02:
            u = clamp((t - T.T_BANGA0) / (T.T_STOP - T.T_BANGA0))
            glow(canvas, rim_s[0], rim_s[1], (110 + 330 * u ** 1.5) * z, (120, 220, 255), 0.35 + 0.65 * u)
        elif t < T.T_POP:
            glow(canvas, rim_s[0], rim_s[1], (430 + 40 * math.sin(t * 40)) * z, (150, 235, 255), 0.85)
        else:
            u = (t - T.T_POP) / 0.25
            glow(canvas, rim_s[0], rim_s[1], 520 * z * (1 - u * 0.4), (200, 250, 255), 1.0 - u)

    # Funken aus dem Eimer beim Banga
    if T.T_BANGA0 < t < T.T_POP + 0.3:
        te = T.T_BANGA0
        k = 0
        while te < min(t, T.T_STOP):
            Wd.sparks(fx, cam, (RIM[0], RIM[1] - 30), t - te, 300 + k, n=9, speed=620, life=0.55,
                      color=(140, 230, 255), gravity=1100, spread=(200, 340), size=5)
            te += 0.055
            k += 1
    # Speedlines beim Banga
    if T.T_BANGA0 + 0.05 < t < T.T_STOP:
        c = cam.pt(*HEAD_C)
        Wd.speed_lines(fx, c, t, 11, n=44, r0=380 * z * 0.8, r1=1800, color=(150, 156, 160), thick=7,
                       strength=0.55 + 0.45 * a)

    # Idee-Ausrufezeichen
    if T.T_IDEA <= t < T.T_IDEA + 0.42:
        u = (t - T.T_IDEA) / 0.42
        s_ = e_back(min(1, u / 0.25), 2.6) * (1 - smooth((u - 0.8) / 0.2))
        spr = text_sprite("!", 260, (255, 226, 60), 12, (40, 20, 50))
        c = cam.pt(BX + 120, BY - 1030 * BS)
        h_, w_ = spr.shape[:2]
        blit(canvas, spr, Tm(*c) @ Rm(-8 * (1 - min(1, u / 0.25))) @ Sm(s_ * z * 0.9) @ Tm(-w_ / 2, -h_ / 2))

    # Glint am Eimer (bucketo)
    if T.V_BUCKETO + 0.02 <= t < T.V_BUCKETO + 0.30:
        u = (t - T.V_BUCKETO - 0.02) / 0.28
        c = cam.pt(BX + (700 - 470) * BS, BY - (1411 - 1140) * BS)
        Wd.burst_star(fx, c, 110 * z * math.sin(u * math.pi), 14 * z, 4, math.radians(20 * u), (255, 255, 255))

    # Kick-Swoosh + Staub
    if T.T_KICK <= t < T.T_KICK + 0.16:
        u = (t - T.T_KICK) / 0.16
        c = cam.pt(BX - 250, BY - 60)
        pts = [(c[0] + math.cos(math.radians(a_)) * 170 * z, c[1] + math.sin(math.radians(a_)) * 110 * z)
               for a_ in np.linspace(120 + 40 * u, 230 + 40 * u, 14)]
        for i in range(len(pts) - 1):
            fx.line(pts[i], pts[i + 1], (int(255 * (1 - u)),) * 3, 12 * (1 - u) * z + 2)
    if T.T_KICK <= t < T.T_KICK + 0.4:
        c = (PH_REST[0], PH_REST[1] + 118)
        Wd.sparks(fx, cam, c, t - T.T_KICK, 61, n=10, speed=260, life=0.4, color=(120, 130, 150), gravity=200,
                  spread=(190, 350), size=7)

    # Landung: Funken/Sterne am Eimerrand
    if T.T_LAND <= t < T.T_LAND + 0.4:
        Wd.sparks(fx, cam, (RIM[0], RIM[1] - 10), t - T.T_LAND, 71, n=12, speed=480, life=0.35,
                  color=(90, 220, 255), gravity=1200, spread=(210, 330), size=5)

    # POP: Ring + Stern
    if T.T_POP <= t < T.T_POP + 0.5:
        u = (t - T.T_POP) / 0.5
        c = cam.pt(RIM[0], RIM[1] - 30)
        Wd.shock_ring(fx, c, 80 + 1100 * e_out(u, 3) * z, 26 * (1 - u) + 2, (int(255 * (1 - u)),) * 3)
        Wd.burst_star(fx, c, 340 * z * (1 - u), 60 * z, 9, u, (int(255 * (1 - u)),) * 3)
        Wd.sparks(fx, cam, (RIM[0], RIM[1] - 30), t - T.T_POP, 81, n=40, speed=1100, life=0.6, color=(180, 240, 255),
                  gravity=700, spread=(180, 360), size=6)

    # Blitze vom Handy
    if ph is not None and ph["mode"] == "charge" and t > T.T_POP + 0.10:
        pc = cam.pt(ph["cx"], ph["cy"])
        seedb = int(t * 15) * 13
        k = clamp((ph["pct"] - 100) / 9900.0)
        tg = [BANANA_TOP, (HEAD_C[0] - 120, HEAD_C[1] + 30)]
        if t < T.T_BULB:
            tg.append(bulb_pos)
        if t < T.T_FRAME_FALL + 0.1:
            tg.append((Wd.PIC[0] + 120, Wd.PIC[1] + 150))
        r_ = rng(seedb)
        for j in range(2):
            tg.append((float(r_.uniform(80, 1000)), 1340.0))
        nb = 2 + int(k * 3)
        for j in range(min(nb, len(tg))):
            tx = tg[(j + int(t * 15)) % len(tg)]
            Wd.draw_bolt(fx, pc, cam.pt(*tx), seedb + j * 7, width=4 + 5 * k, color=(255, 190, 90) if j % 2 else (255, 230, 150))

    # Glasscherben (Gluehbirne platzt)
    if t >= T.T_BULB:
        Wd.sparks(fx, cam, bulb_pos, t - T.T_BULB, 91, n=34, speed=700, life=0.7, color=(200, 240, 255), gravity=1500,
                  size=5)
        if t < T.T_BULB + 0.12:
            c = cam.pt(*bulb_pos)
            Wd.burst_star(fx, c, 320 * z * (1 - (t - T.T_BULB) / 0.12), 40 * z, 8, 0.3, (255, 255, 255))

    fx.apply(canvas, sigma=8 * z ** 0.5)

    # Rauch in dunklem Raum
    if t >= T.T_DARK_ROOM - 0.05:
        for i in range(5):
            age = ((t * 0.55 + i * 0.2) % 1.0)
            c = cam.pt(BANANA_TOP[0] - 6 + 20 * math.sin(age * 5 + i), BANANA_TOP[1] - 30 - age * 260)
            glow(canvas, c[0], c[1], (30 + age * 70) * z, (56, 58, 62), 0.42 * (1 - age), power=1.4, additive=False)

    # Stroboskop-Blitzlicht
    if T.T_POP + 0.12 < t < T.T_WHITE0 and int(t * 30) % 3 == 0:
        overlay_white(canvas, 0.20)

    # Vignette + Weiss-/Invert-Flash
    from engine import vignette
    vignette(canvas, 0.35)
    if T.T_BANGA0 + 0.04 < t < T.T_STOP and int(t * 30) % 3 == 0:
        overlay_white(canvas, 0.10)
    if T.T_POP <= t < T.T_POP + 0.07:
        canvas[:] = 255 - canvas
    elif T.T_POP + 0.07 <= t < T.T_POP + 0.16:
        overlay_white(canvas, 0.55 * (1 - (t - T.T_POP - 0.07) / 0.09))
    if T.T_WHITE0 <= t < T.T_EXT:
        overlay_white(canvas, smooth((t - T.T_WHITE0) / 0.18) * 1.0)

    # Whip-Motion-Blur
    c0, c1 = camera(t - 0.02), camera(t + 0.02)
    vx = (c1.cx - c0.cx) * cam.z / 0.04 / 30.0 * 1.0
    vy = (c1.cy - c0.cy) * cam.z / 0.04 / 30.0 * 1.0
    speed = math.hypot(vx, vy)
    if speed > 6 and t < T.T_WHIP1 + 0.02:
        motion_blur(canvas, -vx * 0.9, -vy * 0.9)
    return canvas


# ============================================================================
# Aussenansicht: Stadt
# ============================================================================
CITY_RECT = (0, 200, W, 1090)          # Basis der Skyline = Bodenlinie y=1290


def exterior_frame(t, ctx, final=False):
    canvas = np.zeros((H, W, 3), np.uint8)
    house_x, house_y = 540, 1290
    RH = CITY_RECT[3]
    ctx.city.src = (0.5, 0.90)
    bt = T.T_BLACKOUT if not final else -10.0
    # Himmel oberhalb des Stadt-Rechtecks: Verlauf fortsetzen
    sky_top = np.array((46, 14, 12), np.float32)
    sky_mid = np.array((110, 44, 70), np.float32)
    yy = np.linspace(0, 1, CITY_RECT[1] + 1)[:, None, None]
    canvas[:CITY_RECT[1] + 1] = (sky_top + (sky_mid - sky_top) * yy ** 1.2).astype(np.uint8)
    ctx.city.draw(canvas, CITY_RECT, blackout_t=bt, t=t, speed=0.55, relight_t=(T.T_EXT2 + 0.25 if final else None))
    cv2.rectangle(canvas, (0, house_y), (W, H), (34, 20, 16), -1)
    cv2.line(canvas, (0, house_y), (W, house_y), (60, 36, 30), 3, cv2.LINE_AA)

    # Haus (Silhouette) mit Fenster
    hw_, hh_ = 220, 160
    from engine import aa_poly
    house = [(house_x - hw_ / 2, house_y), (house_x - hw_ / 2, house_y - hh_), (house_x, house_y - hh_ - 100),
             (house_x + hw_ / 2, house_y - hh_), (house_x + hw_ / 2, house_y)]
    aa_poly(canvas, house, (26, 14, 12))
    aa_poly(canvas, [(house_x + 56, house_y - hh_ - 20), (house_x + 56, house_y - hh_ - 100),
                     (house_x + 86, house_y - hh_ - 100), (house_x + 86, house_y - hh_ + 4)], (26, 14, 12))
    wcol = (255, 240, 200) if not final else (255, 226, 176)
    wx0, wy0, wx1, wy1 = house_x - 36, house_y - 120, house_x + 36, house_y - 46
    cv2.rectangle(canvas, (wx0, wy0), (wx1, wy1), wcol, -1)
    cv2.line(canvas, (house_x, wy0), (house_x, wy1), (40, 24, 30), 4, cv2.LINE_AA)
    cv2.line(canvas, (wx0, (wy0 + wy1) // 2), (wx1, (wy0 + wy1) // 2), (40, 24, 30), 4, cv2.LINE_AA)
    wc = (house_x, (wy0 + wy1) // 2)

    fx = Wd.FX()
    if not final:
        te = t - T.T_EXT
        if te < 0.65:
            u = te / 0.65
            wdt = 74 * (1 - u) ** 0.7 + 8
            bx = wc[0]
            fx.poly([(bx - wdt, wc[1]), (bx + wdt, wc[1]), (bx + wdt * 0.35, -80), (bx - wdt * 0.35, -80)],
                    (int(255 * (1 - u ** 2)),) * 3)
            for j in range(3):
                Wd.draw_bolt(fx, wc, (bx + (j - 1) * 160 * (1 - u), -60), int(t * 15) * 5 + j, width=6 * (1 - u) + 2)
        tw = t - T.T_BLACKOUT
        if tw > 0:
            radius = tw * RH / (0.55 * 1.7)
            Wd.shock_ring(fx, wc, radius, 12 * max(0.15, 1 - radius / 2600), (int(255 * max(0, 1 - radius / 2500)),) * 3)
    else:
        te = t - T.T_EXT2
        fl = 1.0 if int(te * 24) % 9 != 4 else 0.7
        glow(canvas, wc[0], wc[1], 230, (255, 235, 190), 0.6 * fl)
    fx.apply(canvas, sigma=10, glow_gain=1.2)

    if not final:
        z = 1.0 + 0.10 * clamp((t - T.T_EXT) / 1.0)
        sx, sy = _imp(t, T.T_EXT, 26, 9, 9)
        zoom_canvas(canvas, z, sx, sy, wc[0], wc[1])
        overlay_white(canvas, 1 - smooth((t - T.T_EXT) / 0.14))
    else:
        u = clamp((t - T.T_EXT2) / (T.T_END - T.T_EXT2))
        z = 1.0 + 0.55 * e_out(u, 1.6)
        zoom_canvas(canvas, z, 0, 0, wc[0], wc[1] - 60)
    from engine import vignette
    vignette(canvas, 0.45)
    return canvas


def render_frame(t, ctx):
    if T.T_EXT <= t < T.T_DARK_ROOM:
        return exterior_frame(t, ctx, False)
    if t >= T.T_EXT2:
        return exterior_frame(t, ctx, True)
    return room_frame(t, ctx)

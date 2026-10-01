"""Synthetisierte Soundeffekte (numpy/scipy) - keine externen Samples, voll reproduzierbar.

Alle Funktionen liefern mono float32 bei 48 kHz, Spitzen ca. +-1.
"""
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000


def _n(d):
    return int(d * SR)


def tt(d):
    return np.arange(_n(d)) / SR


def rng(seed):
    return np.random.default_rng(seed)


def lp(x, fc, order=4):
    return sosfilt(butter(order, min(fc, SR / 2 - 100), "low", fs=SR, output="sos"), x)


def hp(x, fc, order=4):
    return sosfilt(butter(order, fc, "high", fs=SR, output="sos"), x)


def bp(x, lo, hi, order=3):
    return sosfilt(butter(order, [lo, min(hi, SR / 2 - 100)], "band", fs=SR, output="sos"), x)


def env(d, a=0.002, tau=0.1):
    t = tt(d)
    e = np.exp(-t / tau)
    an = max(1, int(a * SR))
    e[:an] *= np.linspace(0, 1, an)
    return e


def sweep(f0, f1, d, expo=True, harm=()):
    t = tt(d)
    f = f0 * (f1 / f0) ** (t / d) if expo else f0 + (f1 - f0) * t / d
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph)
    for k, a in harm:
        y += a * np.sin(k * ph)
    return y


def tone(f, d, tau=0.08, a=0.002, harm=((2, 0.25), (3, 0.08))):
    t = tt(d)
    y = np.sin(2 * np.pi * f * t)
    for k, amp in harm:
        y += amp * np.sin(2 * np.pi * f * k * t)
    return y * env(d, a, tau)


def fade(x, a=0.004, b=0.004):
    x = x.copy()
    na, nb = int(a * SR), int(b * SR)
    if na:
        x[:na] *= np.linspace(0, 1, na)
    if nb:
        x[-nb:] *= np.linspace(1, 0, nb)
    return x


def norm(x, peak=1.0):
    m = np.max(np.abs(x)) + 1e-9
    return (x / m * peak).astype(np.float32)


# ----------------------------------------------------------------------------
def ping():
    """Low-Battery-Alert: zwei kurze Toene."""
    y = np.zeros(_n(0.34))
    a = tone(988, 0.11, 0.06)
    b = tone(1318, 0.16, 0.08)
    y[:len(a)] += a
    o = _n(0.12)
    y[o:o + len(b)] += b
    return norm(y, 0.8)


def power_down():
    d = 0.42
    y = sweep(900, 45, d, harm=((2, 0.3), (3, 0.15))) * env(d, 0.001, 0.14)
    sq = np.sign(sweep(700, 50, d)) * 0.22 * env(d, 0.001, 0.12)
    click = lp(rng(1).standard_normal(_n(d)), 5000) * env(d, 0.0005, 0.006) * 1.2
    thump = sweep(120, 40, d) * env(d, 0.001, 0.09) * 0.9
    return norm(y + sq + click + thump, 0.9)


def whoosh(d=0.3, f0=400, f1=3000, peak=0.6, rise=0.5):
    n = _n(d)
    noise = rng(3).standard_normal(n)
    out = np.zeros(n)
    blk = 512
    zi = None
    for i in range(0, n, blk):
        u = i / max(n, 1)
        fc = f0 * (f1 / f0) ** u
        sos = butter(2, [max(60, fc * 0.6), min(SR / 2 - 200, fc * 1.6)], "band", fs=SR, output="sos")
        seg, _ = sosfilt(sos, noise[i:i + blk], zi=np.zeros((sos.shape[0], 2)))
        out[i:i + blk] = seg
    t = np.arange(n) / n
    e = np.sin(np.pi * np.clip(t ** rise, 0, 1)) ** 1.5
    return norm(out * e, peak)


def boing(f0=260, d=0.5):
    t = tt(d)
    f = f0 * (1.9 - 0.9 * (1 - np.exp(-t / 0.10))) * (1 + 0.07 * np.sin(2 * np.pi * 9 * t) * np.exp(-t / 0.3))
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = (np.sin(ph) + 0.35 * np.sin(2 * ph) + 0.15 * np.sin(3 * ph)) * env(d, 0.003, 0.17)
    return norm(y, 0.7)


def bell(f=1568, d=0.9, peak=0.6):
    t = tt(d)
    y = np.zeros_like(t)
    for k, a, tau in ((1, 1, 0.45), (2.76, 0.55, 0.3), (5.4, 0.3, 0.2), (8.9, 0.15, 0.12)):
        y += a * np.sin(2 * np.pi * f * k * t) * np.exp(-t / tau)
    return norm(y * env(d, 0.001, 10), peak)


def thunk(f0=200, f1=70, d=0.22, tau=0.07, click=0.6):
    y = sweep(f0, f1, d) * env(d, 0.001, tau)
    c = lp(rng(5).standard_normal(_n(d)), 3500) * env(d, 0.0005, 0.008) * click
    return norm(y + c, 0.9)


def kick_hit():
    a = thunk(150, 55, 0.25, 0.07, 0.9)
    w = whoosh(0.22, 900, 5000, 0.5, 0.35)
    y = np.zeros(_n(0.3))
    y[:len(a)] += a
    y[:len(w)] += w * 0.8
    return norm(y, 0.9)


def plunk():
    """Handy faellt in den Plastikeimer."""
    d = 0.45
    y = sweep(260, 120, d) * env(d, 0.001, 0.09)
    rattle = bp(rng(7).standard_normal(_n(d)), 900, 3800) * env(d, 0.001, 0.05) * 0.6
    y2 = np.zeros(_n(d))
    for k, (dt, g) in enumerate(((0.0, 1.0), (0.085, 0.5), (0.15, 0.3))):
        o = _n(dt)
        seg = (tone(420 - 60 * k, 0.12, 0.03) * g * 0.35)
        y2[o:o + len(seg)] += seg[:len(y2) - o]
    return norm(y + rattle + y2, 0.9)


def bonk(f=210, d=0.12):
    y = sweep(f * 1.25, f * 0.8, d) * env(d, 0.0008, 0.035)
    c = bp(rng(int(f)).standard_normal(_n(d)), 1200, 5000) * env(d, 0.0004, 0.012) * 0.7
    return norm(y + c, 0.9)


def hum_rise(d, f0=90, f1=1100, g0=0.15, g1=1.0):
    t = tt(d)
    f = f0 * (f1 / f0) ** (t / d)
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.33 * np.sin(3 * ph) + 0.2 * np.sin(5 * ph)
    y *= np.sign(np.sin(ph * 0.5 * 2)) * 0.3 + 0.7
    amp = g0 + (g1 - g0) * (t / d) ** 1.6
    return norm(y * amp, 0.8)


def crackle(d, density=0.5, seed=11, lo=1200, hi=9000):
    n = _n(d)
    r = rng(seed)
    base = bp(r.standard_normal(n), lo, hi)
    blk = int(0.0025 * SR)
    gate = (r.random(n // blk + 2) < density).astype(float)
    g = np.repeat(gate, blk)[:n]
    g = np.convolve(g, np.ones(40) / 40, mode="same")
    y = base * g
    y += 0.3 * lp(r.standard_normal(n), 300) * np.convolve(g, np.ones(400) / 400, mode="same")
    return norm(y, 0.9)


def zap(d=0.25, seed=21):
    y = crackle(d, 0.75, seed, 1500, 12000)
    y += 0.5 * sweep(3500, 300, d) * env(d, 0.0005, 0.06)
    return norm(y * env(d, 0.0005, d / 2.5), 0.95)


def boom(d=1.0, f0=110, f1=28):
    y = sweep(f0, f1, d) * env(d, 0.002, 0.30)
    nz = lp(rng(13).standard_normal(_n(d)), 900) * env(d, 0.001, 0.28) * 0.9
    return norm(y + nz, 1.0)


def glass(seed=31, d=0.7, n=40):
    r = rng(seed)
    y = np.zeros(_n(d))
    for _ in range(n):
        t0 = r.uniform(0, d * 0.75)
        f = r.uniform(2500, 9500)
        dd = r.uniform(0.04, 0.16)
        seg = tone(f, dd, dd / 4, harm=()) * r.uniform(0.2, 1.0)
        o = _n(t0)
        seg = seg[:len(y) - o]
        y[o:o + len(seg)] += seg
    y += hp(rng(seed + 1).standard_normal(_n(d)), 4000) * env(d, 0.0005, 0.03) * 0.9
    return norm(y, 0.8)


def bulb_pop():
    d = 0.8
    y = np.zeros(_n(d))
    pop = hp(rng(41).standard_normal(_n(0.06)), 1800) * env(0.06, 0.0002, 0.012)
    y[:len(pop)] += pop * 1.2
    g = glass(32, 0.7)
    y[:len(g)] += g * 0.7
    z = zap(0.18, 43)
    y[:len(z)] += z * 0.9
    b = thunk(160, 60, 0.3, 0.09, 0.3)
    y[:len(b)] += b * 0.8
    return norm(y, 0.95)


def relay_click(seed=0, g=1.0):
    n = _n(0.05)
    c = bp(rng(seed).standard_normal(n), 900, 4200) * env(0.05, 0.0002, 0.006)
    t = tone(170, 0.05, 0.01, harm=()) * 0.5
    return norm(c + t, 0.8 * g)


def city_powerdown(d=1.1):
    y = sweep(1600, 38, d, harm=((2, 0.4),)) * env(d, 0.01, 0.55)
    y += 0.35 * hum_rise(d, 60, 30, 1.0, 0.0)[: _n(d)] if False else 0
    return norm(y, 0.7)


def riser(d=0.3, f0=200, f1=4000):
    t = tt(d)
    y = sweep(f0, f1, d) * (t / d) ** 1.4
    y += 0.3 * bp(rng(51).standard_normal(_n(d)), 800, 6000) * (t / d) ** 2
    return norm(y, 0.8)


def tinnitus(d=1.0, f=6400):
    t = tt(d)
    y = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.55)
    return norm(y, 0.25)


def room_tone(d, seed=61):
    n = tt(d)
    b = np.cumsum(rng(seed).standard_normal(len(n)))
    b = hp(b, 25)
    b = lp(b / (np.max(np.abs(b)) + 1e-9), 400)
    return norm(b, 0.05)


def notif():
    y = np.zeros(_n(0.5))
    a = tone(880, 0.16, 0.08)
    b = tone(1320, 0.3, 0.14)
    y[:len(a)] += a
    o = _n(0.11)
    y[o:o + len(b)] += b[:len(y) - o]
    return norm(y, 0.7)


def sad_trombone():
    d = 0.8
    t = tt(d)
    f = np.where(t < 0.22, 311, np.where(t < 0.44, 294, np.where(t < 0.62, 277, 262 * (1 - 0.06 * np.sin(2 * np.pi * 6 * (t - 0.62))))))
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.35 * np.sin(3 * ph)
    y = lp(y, 1800) * np.minimum(1, t / 0.03) * np.exp(-np.maximum(0, t - 0.55) / 0.12)
    return norm(y, 0.55)


def cricket(d=2.0, seed=71):
    t = tt(d)
    y = np.zeros_like(t)
    for k in range(int(d / 0.42) + 1):
        t0 = k * 0.42
        for j in range(3):
            o = _n(t0 + j * 0.07)
            seg = np.sin(2 * np.pi * 4700 * tt(0.045)) * np.hanning(_n(0.045))
            seg = seg[:max(0, len(y) - o)]
            y[o:o + len(seg)] += seg
    return norm(y, 0.12)


def bark(seed=81):
    d = 0.5
    y = np.zeros(_n(d))
    for (t0, f0) in ((0.0, 340), (0.2, 300)):
        dd = 0.13
        t = tt(dd)
        f = f0 * (1 - 0.3 * t / dd)
        ph = 2 * np.pi * np.cumsum(f) / SR
        src = np.sign(np.sin(ph)) * 0.5 + np.sin(ph) * 0.5
        src = bp(src, 450, 1700) * np.sin(np.pi * np.clip(t / dd, 0, 1)) ** 0.6
        o = _n(t0)
        y[o:o + len(src)] += src
    return norm(lp(y, 2500), 0.6)


def reverb(x, d=1.4, wet=0.5, seed=91, lpf=3000):
    r = rng(seed)
    n = _n(d)
    ir = r.standard_normal(n) * np.exp(-np.arange(n) / SR / (d / 5))
    ir = lp(ir, lpf)
    wetx = fftconvolve(x, ir)[:len(x) + n // 2]
    out = np.zeros(len(wetx))
    out[:len(x)] += x * (1 - wet)
    out += wetx / (np.max(np.abs(wetx)) + 1e-9) * wet * np.max(np.abs(x))
    return out.astype(np.float32)

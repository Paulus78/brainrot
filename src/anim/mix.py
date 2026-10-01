"""Audio-Mix: Bongo-Stimme (edge-tts, hoch geshiftet) + synthetisierte SFX auf der Timeline.

  python src/anim/mix.py out.wav
"""
import asyncio
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import sfx  # noqa: E402
import timeline as TL  # noqa: E402

SR = sfx.SR
EP = TL.EP


class Bus:
    def __init__(self, dur):
        self.n = int(dur * SR)
        self.l = np.zeros(self.n, np.float32)
        self.r = np.zeros(self.n, np.float32)

    def add(self, t, sig, g=1.0, pan=0.0):
        sig = np.asarray(sig, np.float32)
        o = int(round(t * SR))
        if o >= self.n:
            return
        if o < 0:
            sig = sig[-o:]
            o = 0
        m = min(len(sig), self.n - o)
        a = (pan + 1) * np.pi / 4
        self.l[o:o + m] += sig[:m] * g * np.cos(a) * 1.414
        self.r[o:o + m] += sig[:m] * g * np.sin(a) * 1.414


def load_voice(key):
    p = TL.VOICE_DIR / f"{TL.VOICE_FILES[key]}.wav"
    x, _ = TL._load_wav(p, SR)
    return x


def ensure_crowd():
    """Ferne Menge ruft (edge-tts, danach tiefpassgefiltert + Hall)."""
    import edge_tts
    d = EP / "audio" / "crowd"
    d.mkdir(parents=True, exist_ok=True)
    jobs = [("c1", "en-US-ChristopherNeural", "NOOOOO!", "+10Hz", "-15%"),
            ("c2", "en-US-AnaNeural", "My Wi-Fi!", "+30Hz", "+0%"),
            ("c3", "es-ES-ElviraNeural", "¡Mi serie!", "+20Hz", "-5%"),
            ("c4", "es-MX-JorgeNeural", "¡No, no, no!", "+0Hz", "+10%")]

    async def one(name, voice, text, pitch, rate):
        out = d / f"{name}.mp3"
        if not out.exists():
            await edge_tts.Communicate(text, voice, rate=rate, pitch=pitch).save(str(out))
        return out

    async def all_():
        return await asyncio.gather(*[one(*j) for j in jobs])

    paths = asyncio.run(all_())
    sigs = []
    for p in paths:
        x, _ = TL._load_wav(p, SR)
        sigs.append(x)
    return sigs


def duck_curve(n, intervals, depth=0.45, ramp=0.03):
    g = np.ones(n, np.float32)
    for a, b in intervals:
        i0, i1 = int(max(0, a) * SR), int(min(n / SR, b) * SR)
        g[i0:i1] = depth
    k = int(ramp * SR)
    if k > 1:
        g = np.convolve(g, np.ones(k) / k, mode="same")
    return g


def build(out_path):
    dur = TL.T_END + 0.6
    sfx_bus = Bus(dur)
    voice_bus = Bus(dur)
    T = TL

    # ---------------- Hook: Low-Battery ----------------
    p = sfx.ping()
    sfx_bus.add(T.T_PING1, p, 0.85)
    sfx_bus.add(T.T_PING2, p, 0.85)
    sfx_bus.add(T.T_DIE, sfx.power_down(), 1.0)
    sfx_bus.add(T.T_DIE + 0.02, sfx.relay_click(3), 0.6)

    # Whip zu Bongo + Schock-Sprung
    sfx_bus.add(T.T_WHIP0 - 0.06, sfx.whoosh(0.34, 500, 4200, 0.9, 0.6), 0.85)
    sfx_bus.add(0.68, sfx.boing(330, 0.45), 0.55, -0.2)
    sfx_bus.add(T.T_WHIP1 + 0.02, sfx.thunk(140, 60, 0.18, 0.06, 0.2), 0.55)
    sfx_bus.add(1.10, sfx.thunk(190, 95, 0.14, 0.05, 0.3), 0.4)

    # Blick-Foley: kleine Augen-Zips
    for te_, gg in ((1.40, 0.35), (T.T_LOOK_PHONE, 0.4), (T.T_LOOK_BUCKET, 0.5), (2.12, 0.35), (T.T_LAND + 0.2, 0.3)):
        sfx_bus.add(te_, sfx.whoosh(0.09, 1800, 6000, 0.5, 0.5), gg, 0.1)
        sfx_bus.add(te_ + 0.02, sfx.tone(1900, 0.05, 0.02, harm=()), gg * 0.5)

    # Erkenntnis + Bucketo
    sfx_bus.add(T.T_IDEA, sfx.bell(1568, 0.8, 0.6), 0.55)
    sfx_bus.add(T.T_IDEA, sfx.boing(400, 0.3), 0.35)
    sfx_bus.add(T.V_BUCKETO - 0.05, sfx.thunk(240, 95, 0.22, 0.07, 0.7), 0.95)
    sfx_bus.add(T.V_BUCKETO - 0.04, sfx.boing(300, 0.5), 0.5)
    sfx_bus.add(T.V_BUCKETO + 0.04, sfx.bell(2093, 0.7, 0.5), 0.45)

    # Kick + Flug + Landung im Eimer
    sfx_bus.add(T.T_KICK - 0.02, sfx.kick_hit(), 0.95)
    sfx_bus.add(T.T_KICK + 0.04, sfx.whoosh(0.5, 700, 2600, 0.6, 0.7), 0.6, -0.4)
    sfx_bus.add(T.T_LAND - 0.02, sfx.plunk(), 1.0, 0.2)

    # ---------------- BANGA BANGA ----------------
    nb = int((T.T_STOP - T.T_BANGA0) / 0.10)
    for k in range(nb):
        u = k / max(nb - 1, 1)
        f = 190 + 150 * u
        sfx_bus.add(T.T_BANGA0 + k * 0.10, sfx.bonk(f, 0.12), 0.55 + 0.4 * u, -0.3 if k % 2 else 0.3)
    dur_b = T.T_STOP - T.T_BANGA0
    h = sfx.hum_rise(dur_b, 90, 1500, 0.10, 1.0)
    h = sfx.fade(h, 0.02, 0.006)
    sfx_bus.add(T.T_BANGA0, h, 0.55)
    c = sfx.crackle(dur_b, 0.55, 12, 1500, 10000)
    c *= np.linspace(0.1, 1.0, len(c)) ** 1.5
    sfx_bus.add(T.T_BANGA0, sfx.fade(c, 0.02, 0.006), 0.5)

    # Mini-Stille, dann Tick + kurzes Anschwellen
    sfx_bus.add(T.T_STOP + 0.09, sfx.relay_click(9), 0.5)
    sfx_bus.add(T.T_POP - 0.13, sfx.riser(0.13, 300, 3500), 0.6)

    # ---------------- POP + Ueberladung ----------------
    sfx_bus.add(T.T_POP, sfx.boom(1.1, 130, 30), 1.0)
    sfx_bus.add(T.T_POP, sfx.zap(0.32, 22), 0.9)
    sfx_bus.add(T.T_POP, sfx.whoosh(0.45, 300, 7000, 0.8, 0.4), 0.7)
    stage = T.T_WHITE0 - T.T_POP - 0.1
    sfx_bus.add(T.T_POP + 0.1, sfx.fade(sfx.crackle(stage, 0.7, 14, 1200, 9000), 0.01, 0.01), 0.75)
    w = sfx.hum_rise(stage, 220, 4200, 0.25, 1.0)
    sfx_bus.add(T.T_POP + 0.1, sfx.fade(w, 0.01, 0.01), 0.55)
    r = np.random.default_rng(5)
    t = T.T_POP + 0.14
    while t < T.T_WHITE0 - 0.05:
        sfx_bus.add(t, sfx.zap(0.12, int(t * 100)), 0.5, float(r.uniform(-0.6, 0.6)))
        t += float(r.uniform(0.09, 0.17))
    sfx_bus.add(T.T_FRAME_FALL + 0.42, sfx.thunk(140, 50, 0.3, 0.1, 0.8), 0.6, 0.6)
    sfx_bus.add(T.T_FRAME_FALL + 0.44, sfx.glass(33, 0.5, 18), 0.4, 0.5)
    sfx_bus.add(T.T_BULB, sfx.bulb_pop(), 1.0)

    # ---------------- Whiteout -> Stadt-Blackout ----------------
    sfx_bus.add(T.T_WHITE0, sfx.riser(T.T_EXT - T.T_WHITE0, 300, 7000), 0.65)
    sfx_bus.add(T.T_EXT, sfx.boom(1.4, 100, 26), 1.0)
    sfx_bus.add(T.T_EXT, sfx.zap(0.4, 61), 0.8)
    sfx_bus.add(T.T_BLACKOUT, sfx.city_powerdown(1.1), 0.65)
    r = np.random.default_rng(8)
    for k in range(30):
        tk = T.T_BLACKOUT + 0.05 + 0.95 * (r.random() ** 0.8)
        sfx_bus.add(tk, sfx.relay_click(int(k * 7), 1.0), 0.5, float(r.uniform(-0.9, 0.9)))

    # ---------------- Dunkler Raum: Kontrast ----------------
    sfx_bus.add(T.T_DARK_ROOM, sfx.tinnitus(1.2), 0.5)
    sfx_bus.add(T.T_DARK_ROOM, sfx.room_tone(T.T_EXT2 - T.T_DARK_ROOM + 0.2), 1.0)
    sfx_bus.add(T.T_BANNER, sfx.notif(), 0.75)
    sfx_bus.add(T.T_BANNER + 0.30, sfx.sad_trombone(), 0.55)

    # ---------------- Schluss: Stadt ----------------
    crowd = ensure_crowd()
    offs = [0.02, 0.16, 0.30, 0.44]
    for i, x in enumerate(crowd):
        x = sfx.lp(x, 1800)
        x = sfx.reverb(x, 1.6, 0.55, 100 + i, 2200)
        sfx_bus.add(T.T_EXT2 + 0.10 + offs[i], x, 0.55, (-0.6, 0.5, -0.2, 0.7)[i])
    b = sfx.reverb(sfx.bark(), 1.2, 0.5, 120, 2500)
    sfx_bus.add(T.T_EXT2 + 0.9, b, 0.55, 0.6)
    sfx_bus.add(T.T_EXT2 + 0.2, sfx.cricket(T.T_END - T.T_EXT2 + 0.4), 0.8)
    sfx_bus.add(T.T_EXT2, sfx.room_tone(T.T_END - T.T_EXT2 + 0.6, 62), 1.2)

    # ---------------- Stimme ----------------
    intervals = []
    gains = {"no": 1.0, "bucketo": 1.0, "banga1": 1.0, "banga2": 1.05, "perfecto": 1.0, "fixo": 1.0}
    for name, st in T.VOICE_START.items():
        x = load_voice(name)
        voice_bus.add(st, x, gains[name])
        intervals.append((st - 0.04, st + len(x) / SR + 0.06))
    duck = duck_curve(sfx_bus.n, intervals, depth=0.50, ramp=0.05)

    L = sfx_bus.l * duck + voice_bus.l
    R = sfx_bus.r * duck + voice_bus.r
    y = np.stack([L, R], 1)
    y = np.tanh(y * 0.9) / np.tanh(0.9)
    y = y / max(np.max(np.abs(y)), 1e-6) * 0.93
    y16 = (y * 32767).astype(np.int16)
    with wave.open(str(out_path), "wb") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes(y16.tobytes())
    return dur


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else EP / "audio" / "mix.wav"
    out.parent.mkdir(parents=True, exist_ok=True)
    d = build(out)
    print("mix", out, f"{d:.2f}s")

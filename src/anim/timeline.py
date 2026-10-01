"""Zeitplan des Shorts (Sekunden). Wird von Animation UND Audio-Mix gelesen.

Alle Stimmzeiten sind Startzeiten der (getrimmten) Gemini/edge-TTS-Dateien.
"""
import json
import subprocess
from functools import lru_cache
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
EP = ROOT / "episodes" / "ep004_lowbattery"
VOICE_DIR = EP / "audio" / "voice"

# --- Handlung -----------------------------------------------------------------
T_PING1 = 0.0
T_PING2 = 0.36
T_DIE = 0.66            # Handy stirbt (CRT-Kollaps 0.72-0.82)
T_WHIP0, T_WHIP1 = 0.72, 1.04

V_NO = 1.06
T_LOOK_PHONE = 1.62
T_LOOK_BUCKET = 1.92
T_IDEA = 2.00           # Erkenntnis, "!"
V_BUCKETO = 2.14
T_KICK = 2.40
T_LAND = 2.94
V_BANGA1 = 3.34
V_BANGA2 = 3.86
T_BANGA0 = 3.28
T_STOP = 4.46           # harter Stopp
T_POP = 4.74            # Handy schiesst aus dem Eimer
T_BULB = 5.30
T_FRAME_FALL = 5.05
T_WHITE0 = 5.50
T_EXT = 5.72            # Schnitt zur Stadt-Aussenansicht
T_BLACKOUT = 5.84
T_DARK_ROOM = 6.86      # Schnitt zurueck in den dunklen Raum
V_PERFECTO = 7.02
T_BANNER = 8.10
T_EXT2 = 8.42
V_FIXO = 8.86
T_END = 9.90

# --- Voice: Dateien, Laengen, Huellkurven -------------------------------------
VOICE_FILES = {
    "no": "l1_no", "bucketo": "l2_bucketo", "banga1": "l3_banga", "banga2": "l3_banga_b",
    "perfecto": "l4_perfecto", "fixo": "l5_fixo",
}
VOICE_START = {"no": V_NO, "bucketo": V_BUCKETO, "banga1": V_BANGA1, "banga2": V_BANGA2,
               "perfecto": V_PERFECTO, "fixo": V_FIXO}


def _load_wav(path, sr=48000):
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(out, np.float32), sr


@lru_cache(maxsize=None)
def voice_env(name):
    """Lautstaerke-Huellkurve (100 Hz), 0..1, fuer Mundoeffnung."""
    p = VOICE_DIR / f"{VOICE_FILES[name]}.wav"
    if not p.exists():
        return np.zeros(10), 0.0
    x, sr = _load_wav(p)
    hop = sr // 100
    n = len(x) // hop
    rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop + hop // 2] ** 2)) for i in range(n)])
    rms = rms / max(rms.max(), 1e-6)
    # leicht glaetten, damit der Mund nicht flackert
    k = np.array([0.25, 0.5, 0.25])
    rms = np.convolve(rms, k, mode="same")
    return np.clip(rms * 1.25, 0, 1), len(x) / sr


def voice_dur(name):
    return voice_env(name)[1]


def env_at(name, t):
    """Huellkurve zum Zeitpunkt t (absolut); 0 ausserhalb der Zeile."""
    env, dur = voice_env(name)
    tt = t - VOICE_START[name]
    if tt < 0 or tt > dur:
        return 0.0
    i = int(tt * 100)
    return float(env[min(i, len(env) - 1)])


def speaking(t):
    """Name der gerade laufenden Zeile oder None."""
    for n in VOICE_START:
        tt = t - VOICE_START[n]
        if -0.02 <= tt <= voice_dur(n) + 0.05:
            return n
    return None

"""Bongo-Stimme: edge-tts (neuronal, kostenlos, ohne API-Key) + Pitch/Formant-Shift.

Die Zielrichtung: kleines, hoch gestimmtes, energisches Cartoon-Wesen mit
dezentem spanischem Einschlag. Basis ist eine spanische Neuralstimme, damit
"Bongo", "bucketo", "perfecto" und "fixo" natuerlich ausgesprochen werden.
Anschliessend wird per Resampling nach oben transponiert; das verschiebt auch
die Formanten und erzeugt den "kleines Wesen"-Klang.
"""
import argparse
import asyncio
import json
import subprocess
from pathlib import Path

import edge_tts

ROOT = Path(__file__).resolve().parents[2]

# Zeilenweise Sprechregie. pitch/rate sind edge-tts-Parameter vor dem Shift.
LINES = [
    ("l1_no",        "Bongo... no.",        "+55Hz", "+0%"),    # enttaeuscht, flach
    ("l2_bucketo",   "Bongo bucketo.",      "+75Hz", "+12%"),   # geniale Eingebung
    ("l3_banga",     "Bongo banga banga!",  "+85Hz", "+30%"),   # maximale Energie
    ("l4_perfecto",  "Bongo... perfecto.",  "+65Hz", "-8%"),    # staunend, stolz
    ("l5_fixo",      "Bongo fixo.",         "+45Hz", "+8%"),    # trocken, kurz
]

PRESETS = {
    # name: (voice, pitch_offset_hz, rate_offset_pct, semitone_shift)
    "A": ("es-MX-JorgeNeural", 0, 0, 8.0),
    "B": ("es-MX-DaliaNeural", -40, 0, 5.0),
    "C": ("es-ES-AlvaroNeural", 0, 0, 7.5),
    "D": ("es-CO-GonzaloNeural", 0, 0, 7.5),
    "E": ("es-MX-JorgeNeural", 20, 4, 6.5),
}

SR = 48000


async def synth(text, voice, pitch, rate, dst: Path):
    c = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await c.save(str(dst))


def shift_and_clean(src: Path, dst: Path, semitones: float) -> None:
    """Nach oben transponieren (Tempo bleibt), Stille trimmen, Praesenz anheben."""
    ratio = 2.0 ** (semitones / 12.0)
    tempo = 1.0 / ratio
    chain = []
    while tempo < 0.5:           # atempo akzeptiert nur 0.5..100
        chain.append("atempo=0.5")
        tempo /= 0.5
    chain.append(f"atempo={tempo:.6f}")
    # Nur fuehrende/abschliessende Stille trimmen - interne Pausen ("Bongo... no.")
    # sind Comedy-Timing und bleiben erhalten.
    trim = ("silenceremove=start_periods=1:start_silence=0.01:start_threshold=-42dB,"
            "areverse,"
            "silenceremove=start_periods=1:start_silence=0.01:start_threshold=-42dB,"
            "areverse")
    af = (
        f"asetrate={int(SR * ratio)},aresample={SR}," + ",".join(chain) + ","
        "highpass=f=150,"
        "equalizer=f=2600:t=q:w=1.1:g=3.5,"
        "equalizer=f=5200:t=q:w=1.4:g=2.0,"
        "acompressor=threshold=0.06:ratio=4:attack=6:release=120:makeup=2,"
        + trim + ","
        "loudnorm=I=-14:TP=-1.5:LRA=9,"
        f"aresample={SR}"
    )
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(src), "-af", af,
         "-ac", "1", "-ar", str(SR), "-c:a", "pcm_s16le", str(dst)],
        check=True,
    )


def dur(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def build(preset_name: str, outdir: Path) -> dict:
    voice, d_pitch, d_rate, st = PRESETS[preset_name]
    raw = outdir / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    result = {"preset": preset_name, "voice": voice, "semitone_shift": st, "lines": {}}
    for key, text, pitch, rate in LINES:
        p = f"{int(pitch.rstrip('Hz')) + d_pitch:+d}Hz"
        r = f"{int(rate.rstrip('%')) + d_rate:+d}%"
        mp3 = raw / f"{key}.mp3"
        asyncio.run(synth(text, voice, p, r, mp3))
        wav = outdir / f"{key}.wav"
        shift_and_clean(mp3, wav, st)
        result["lines"][key] = {"text": text, "pitch": p, "rate": r,
                                "file": str(wav.relative_to(ROOT)).replace("\\", "/"),
                                "dur": round(dur(wav), 3)}
        print(f"  {key:14s} {result['lines'][key]['dur']:5.2f}s  {p:>7s} {r:>5s}  {text}")
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preset", default=None, help="einzelnes Preset bauen")
    ap.add_argument("--outdir", default="episodes/ep004_lowbattery/audio/voice")
    args = ap.parse_args()

    if args.preset:
        out = ROOT / args.outdir
        out.mkdir(parents=True, exist_ok=True)
        info = build(args.preset, out)
        (out / "voice.json").write_text(json.dumps(info, indent=2))
        return

    # Audition aller Presets
    base = ROOT / "episodes" / "ep004_lowbattery" / "audio" / "auditions"
    all_info = {}
    for name in PRESETS:
        print(f"[{name}] {PRESETS[name][0]}")
        all_info[name] = build(name, base / name)
        # zusammenhaengende Audition-Datei
        lst = base / name / "concat.txt"
        lst.write_text("".join(f"file '{k}.wav'\n" for k, *_ in LINES))
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                        "-i", str(lst), "-c", "copy", str(base / f"audition_{name}.wav")], check=True)
    (base / "auditions.json").write_text(json.dumps(all_info, indent=2))


if __name__ == "__main__":
    main()

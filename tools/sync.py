"""Lippensynchron-Hilfe: richtet eine Stimmzeile am Originalton eines Clips aus.
Die Figur spricht im Flow-Clip schon (mit falscher Stimme) - dort bewegt sich der Mund.
Wir suchen per Huellkurven-Vergleich, wo und wie schnell die neue Zeile am besten darauf passt."""
import subprocess, numpy as np

SR, HOP = 16000, 160   # 10 ms

def _env(args):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error'] + args + ['-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    n = len(x) // HOP
    e = np.sqrt((x[:n * HOP].reshape(n, HOP) ** 2).mean(1) + 1e-9)
    return np.log1p(e * 200)

def align(clip, t0, t1, line_wav, semis=0, stretches=(0.85, 0.9, 0.95, 1.0, 1.05, 1.1, 1.15, 1.2, 1.3)):
    """Gibt (Startzeit im Clip, Dehnfaktor, Guete 0..1) zurueck. Dehnfaktor > 1 = Zeile wird laenger."""
    band = 'highpass=f=250,lowpass=f=3500'
    orig = _env(['-ss', str(t0), '-to', str(t1), '-i', clip, '-af', band])
    r = 2 ** (semis / 12)
    dub = _env(['-i', line_wav, '-af', f'asetrate={int(48000 * r)},aresample=48000,atempo={1 / r:.5f},{band}'])
    # Stille am Rand der Zeile abschneiden, damit der Einsatz zaehlt
    act = np.where(dub > dub.max() * 0.25)[0]; lead = int(act[0]); dub = dub[lead:act[-1] + 1]
    best = (-2, 0, 1.0)
    for s in stretches:
        m = int(len(dub) * s)
        if m >= len(orig) or m < 5: continue
        d = np.interp(np.linspace(0, len(dub) - 1, m), np.arange(len(dub)), dub); d = (d - d.mean()) / (d.std() + 1e-9)
        for off in range(0, len(orig) - m):
            o = orig[off:off + m]; c = float((d * (o - o.mean())).mean() / (o.std() + 1e-9))
            if c > best[0]: best = (c, off, s)
    c, off, s = best
    return t0 + off * HOP / SR - lead * HOP / SR * s, s, c

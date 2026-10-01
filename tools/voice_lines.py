"""Schneidet die fuenf Zeilen aus der einen Stimmaufnahme (voice/voice_1.mp4) -> voice/line_1..5.wav + Zeiten."""
import subprocess, numpy as np, wave, json, sys
SRC = sys.argv[1] if len(sys.argv) > 1 else 'episodes/ep005_bucketfood/voice/voice_1.mp4'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'episodes/ep005_bucketfood/voice'; SR = 48000
raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', SRC, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
hop = int(0.02 * SR); env = np.array([np.sqrt((x[i:i + hop] ** 2).mean()) for i in range(0, len(x) - hop, hop)])
on = env > max(0.012, env.max() * 0.06)
segs, start, gap = [], None, 0
for i, v in enumerate(on):
    if v:
        if start is None: start = i
        gap = 0
    elif start is not None:
        gap += 1
        if gap > 22:                       # > 0.45 s Stille = neue Zeile
            segs.append((start, i - gap)); start = None
if start is not None: segs.append((start, len(on) - 1))
segs = [(a, b) for a, b in segs if (b - a) * 0.02 > 0.3]
info = []
for k, (a, b) in enumerate(segs, 1):
    s0 = max(0, a * hop - int(0.04 * SR)); s1 = min(len(x), (b + 1) * hop + int(0.10 * SR))
    y = x[s0:s1].copy(); y *= 0.7 / (np.abs(y).max() + 1e-9)
    f = int(0.01 * SR); y[:f] *= np.linspace(0, 1, f); y[-f * 3:] *= np.linspace(1, 0, f * 3)
    w = wave.open(f'{OUT}/line_{k}.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((y * 32767).astype(np.int16).tobytes()); w.close()
    # Wortgrenze: laengste leise Stelle im mittleren Teil der Zeile
    e = env[a:b + 1]; n = len(e); mid = slice(int(n * 0.25), int(n * 0.75))
    split = (int(n * 0.25) + int(np.argmin(np.convolve(e, np.ones(4) / 4, 'same')[mid]))) * 0.02 + 0.04
    info.append(dict(line=k, src=(round(s0 / SR, 2), round(s1 / SR, 2)), dur=round(len(y) / SR, 2), split=round(split, 2)))
json.dump(info, open(f'{OUT}/lines.json', 'w'), indent=1); print(info)

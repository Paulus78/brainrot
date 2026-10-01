"""Sichtung von Clips: Standbild-Streifen (2 Bilder/s), Sprach-Karte (0,1 s pro Zeichen, #=Stimme) und erkannter Text.
Aufruf: python tools/review_clips.py <ordner>   ->  <ordner>/_sheet1.jpg, _sheet2.jpg ..."""
import sys, glob, os, subprocess, numpy as np
sys.path.insert(0, 'src/anim'); sys.path.insert(0, 'src/flowrig')
import f0, asr
from PIL import Image, ImageDraw
from faster_whisper import WhisperModel
d = sys.argv[1]; files = sorted(glob.glob(f'{d}/*.mp4')); m = WhisperModel('small.en', device='cpu', compute_type='int8')
strips = []
for p in files:
    j = p[:-4] + '.jpg'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', p, '-vf', 'fps=2,scale=180:-1,tile=16x1', '-frames:v', '1', j])
    strips.append((os.path.basename(p)[:-4], Image.open(j)))
    x, sr = f0.load_mono(p); hop = int(0.1 * sr); n_ = int(0.04 * sr); line = []
    for i in range(0, len(x) - n_, hop):
        s = x[i:i + n_]; rms = np.sqrt((s ** 2).mean()); s2 = s - s.mean(); ac = np.correlate(s2, s2, 'full')[n_ - 1:]; lo, hi = int(sr / 600), int(sr / 100)
        k = lo + np.argmax(ac[lo:hi]); v = ac[k] / (ac[0] + 1e-9)
        line.append('#' if (rms > 0.015 and v > 0.5) else ('.' if rms > 0.015 else ' '))
    print(f'{os.path.basename(p)[:-4]:>6} |' + ''.join(line) + '|  ', ' '.join(f'{w}@{a}' for w, a, b in asr.words(p, m)))
for part in range(0, len(strips), 4):
    sel = strips[part:part + 4]; s = Image.new('RGB', (sel[0][1].width, sum(i.height for _, i in sel))); y = 0
    for n, i in sel:
        s.paste(i, (0, y)); ImageDraw.Draw(s).rectangle([0, y, 50, y + 18], fill='black'); ImageDraw.Draw(s).text((5, y + 3), n, fill='white'); y += i.height
    s.save(f'{d}/_sheet{part // 4 + 1}.jpg', quality=82)

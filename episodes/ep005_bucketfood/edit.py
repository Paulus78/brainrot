"""Schnitt von Folge 5 "Bongo feeds the bucket" aus den Flow-Clips.
Aufruf (im Repo-Ordner): python episodes/ep005_bucketfood/edit.py  ->  output/ep005/bongo_ep005_v1.mp4"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont

EP = 'episodes/ep005_bucketfood'; CL = f'{EP}/clips'; TMP = f'{EP}/tmp'; OUT = 'output/ep005'
W, H, FPS = 1080, 1920, 30

# Einstellung: Clip, Teile (von, bis, Tempo), Untertitel (Text, von, bis) in ORIGINAL-Clipzeit
SHOTS = [
    dict(clip='A2', parts=[(0.30, 5.90, 1.0)], caps=[('BONGO', 4.60, 5.10), ('FOOD.', 5.10, 5.85)]),
    dict(clip='B2', parts=[(0.60, 7.20, 1.0)], caps=[('BONGO…', 5.00, 5.90), ('BANANA?!', 6.25, 7.20)]),
    dict(clip='C2', parts=[(1.80, 6.60, 1.0)], caps=[('BONGO', 2.45, 3.00), ('FIXO.', 3.00, 3.85)]),
    dict(clip='D1', parts=[(0.30, 3.90, 1.0), (3.90, 6.10, 1.5), (6.10, 7.60, 1.0)], caps=[('BONGO…', 6.40, 6.85), ('NO.', 6.85, 7.55)]),
    dict(clip='E1', parts=[(1.00, 6.60, 1.0)], caps=[('BONGO', 1.65, 2.40), ('BUCKETO.', 2.45, 3.60)]),
]
TITLE = ('BONGO FEEDS THE BUCKET', 0.15, 2.4)
END = ('PART 2?', 1.5)          # Text, Dauer am Schluss

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: raise SystemExit(r.stderr[-1500:])

def text_png(path, text, size, y, fill=(255, 255, 255, 255), stroke=10):
    font = ImageFont.truetype('C:/Windows/Fonts/ariblk.ttf', size)
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    w = d.textlength(text, font=font)
    d.text(((W - w) / 2, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=(15, 15, 15, 255))
    im.save(path)

def map_time(parts, t):
    """Original-Clipzeit -> Zeit innerhalb der geschnittenen Einstellung."""
    acc = 0.0
    for a, b, sp in parts:
        if t <= b: return acc + (max(t, a) - a) / sp
        acc += (b - a) / sp
    return acc

def main():
    os.makedirs(TMP, exist_ok=True); os.makedirs(OUT, exist_ok=True)
    segs, caps, t0 = [], [], 0.0
    for si, s in enumerate(SHOTS):
        for pi, (a, b, sp) in enumerate(s['parts']):
            seg = f'{TMP}/s{si}_{pi}.mp4'; d = (b - a) / sp
            vf = f'setpts=(PTS-STARTPTS)/{sp},fps={FPS},scale={W}:{H}:flags=lanczos,unsharp=5:5:0.5'
            af = f'asetpts=PTS-STARTPTS,atempo={sp},aresample=48000,afade=t=in:d=0.03,afade=t=out:st={d - 0.05:.3f}:d=0.05'
            run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(a), '-to', str(b), '-i', f'{CL}/shot_{s["clip"]}.mp4',
                 '-vf', vf, '-af', af, '-t', f'{d:.3f}', '-c:v', 'libx264', '-crf', '14', '-preset', 'fast', '-pix_fmt', 'yuv420p',
                 '-c:a', 'pcm_s16le', '-ac', '2', seg.replace('.mp4', '.mov')])
            segs.append(seg.replace('.mp4', '.mov'))
        for txt, a, b in s['caps']:
            caps.append((txt, t0 + map_time(s['parts'], a), t0 + map_time(s['parts'], b)))
        t0 += sum((b - a) / sp for a, b, sp in s['parts'])
    total = t0
    # Lautheit je Einstellung angleichen passiert nach dem Zusammenfuegen per loudnorm (ein Durchgang reicht hier)
    with open(f'{TMP}/list.txt', 'w') as f:
        for s in segs: f.write(f"file '{os.path.abspath(s).replace(chr(92), '/')}'\n")
    run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{TMP}/list.txt', '-c', 'copy', f'{TMP}/cut.mov'])

    overlays = [(TITLE[0], TITLE[1], TITLE[2], 60, 215, (255, 225, 60, 255))]
    overlays += [(t, a, b, 118, 1330, (255, 255, 255, 255)) for t, a, b in caps]
    overlays += [(END[0], total - END[1], total, 150, 760, (255, 225, 60, 255))]
    inputs, fc, last = [], [], '0:v'
    for i, (txt, a, b, size, y, col) in enumerate(overlays):
        p = f'{TMP}/cap{i}.png'; text_png(p, txt, size, y, col); inputs += ['-i', p]
        fc.append(f"[{last}][{i + 1}:v]overlay=enable='between(t,{a:.2f},{b:.2f})'[v{i}]"); last = f'v{i}'
    n = len(overlays) + 1
    # leiser Raumton unter allem, damit die Tonspuren der Clips nicht hoerbar wechseln
    fc.append(f"anoisesrc=color=brown:amplitude=0.012:duration={total:.2f}:sample_rate=48000,lowpass=f=900,pan=stereo|c0=c0|c1=c0[bed]")
    fc.append(f"[0:a]dynaudnorm=f=250:g=15:p=0.7:m=6[dia];[dia][bed]amix=inputs=2:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=9,afade=t=out:st={total - 0.25:.2f}:d=0.25[a]")
    out = f'{OUT}/bongo_ep005_v1.mp4'
    run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{TMP}/cut.mov'] + inputs + ['-filter_complex', ';'.join(fc), '-map', f'[{last}]', '-map', '[a]',
         '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
         '-movflags', '+faststart', '-t', f'{total:.2f}', out])
    run(['ffmpeg', '-y', '-loglevel', 'error', '-i', out, '-vf', f'fps=1,scale=216:-1,tile={int(total) + 1}x1', '-frames:v', '1', f'{OUT}/bongo_ep005_v1_sheet.jpg'])
    print('ok', out, f'{total:.2f}s'); print([(round(a, 2), round(b, 2)) for _, a, b in caps])

if __name__ == '__main__':
    main()

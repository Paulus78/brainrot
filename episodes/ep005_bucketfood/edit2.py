"""Schnitt V2 von Folge 5 "Bongo feeds the bucket".
Bild: Flow-Clips mit Start- und Endbild (clips2). Stimme: fuenf Zeilen aus EINER Aufnahme (voice/line_N.wav),
die an der Sprechstelle ueber den Clip gelegt werden; der Originalton des Clips wird dort stummgeschaltet.
Aufruf (im Repo-Ordner): python episodes/ep005_bucketfood/edit2.py  ->  output/ep005/bongo_ep005_v2.mp4"""
import os, json, subprocess
from PIL import Image, ImageDraw, ImageFont

EP = 'episodes/ep005_bucketfood'; CL = f'{EP}/clips2'; VO = f'{EP}/voice'; TMP = f'{EP}/tmp2'; OUT = 'output/ep005'
W, H, FPS = 1080, 1920, 30
NAME = 'bongo_ep005_v2'

# clip, Schnitt (von, bis), Sprechstelle im Clip (mute_von, mute_bis), Zeile + Startzeit, Untertitel-Woerter
SHOTS = [
    dict(clip='A1', cut=(0.20, 6.40), mute=(4.85, 6.30), line=1, at=5.00, words=('BONGO', 'FOOD.')),
    dict(clip='B2', cut=(0.50, 7.10), mute=(5.35, 6.90), line=2, at=5.50, words=('BONGO…', 'BANANA?!')),
    dict(clip='C2', cut=(0.10, 4.55), mute=(0.10, 1.60), line=3, at=0.40, words=('BONGO', 'FIXO.')),
    dict(clip='D5', cut=(1.00, 6.40), mute=(4.85, 6.40), line=4, at=4.95, words=('BONGO…', 'NO.')),
    dict(clip='E7', cut=(0.40, 7.60), mute=(1.75, 3.50), line=5, at=1.90, words=('BONGO', 'BUCKETO.')),
]
TITLE = ('BONGO FEEDS THE BUCKET', 0.15, 2.4)
END = ('PART 2?', 1.3)

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: raise SystemExit(r.stderr[-1500:])

def text_png(path, text, size, y, fill=(255, 255, 255, 255), stroke=10):
    font = ImageFont.truetype('C:/Windows/Fonts/ariblk.ttf', size)
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    w = d.textlength(text, font=font)
    d.text(((W - w) / 2, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=(15, 15, 15, 255))
    im.save(path)

def main():
    os.makedirs(TMP, exist_ok=True); os.makedirs(OUT, exist_ok=True)
    lines = {l['line']: l for l in json.load(open(f'{VO}/lines.json'))}
    segs, caps, t0 = [], [], 0.0
    for si, s in enumerate(SHOTS):
        a, b = s['cut']; d = b - a; L = lines[s['line']]
        m0, m1 = s['mute'][0] - a, s['mute'][1] - a; at = s['at'] - a
        seg = f'{TMP}/s{si}.mov'
        vf = f'setpts=PTS-STARTPTS,fps={FPS},scale={W}:{H}:flags=lanczos,unsharp=5:5:0.5'
        # Originalton: an der Sprechstelle weich aus- und wieder einblenden; Stimme aus der einen Aufnahme dazu
        fade = 0.06
        vol = (f"volume='if(between(t,{m0:.3f},{m1:.3f}),0,if(between(t,{m0 - fade:.3f},{m0:.3f}),({m0:.3f}-t)/{fade},"
               f"if(between(t,{m1:.3f},{m1 + fade:.3f}),(t-{m1:.3f})/{fade},1)))':eval=frame")
        fc = (f"[0:a]asetpts=PTS-STARTPTS,aresample=48000,{vol},afade=t=in:d=0.03,afade=t=out:st={d - 0.05:.3f}:d=0.05,volume=0.9[sfx];"
              f"[1:a]aresample=48000,adelay={int(at * 1000)}:all=1,volume=1.5[vo];"
              f"[sfx][vo]amix=inputs=2:normalize=0:duration=first,pan=stereo|c0=c0|c1=c0[a]")
        run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(a), '-to', str(b), '-i', f'{CL}/v2_{s["clip"]}.mp4', '-i', f'{VO}/line_{s["line"]}.wav',
             '-filter_complex', fc, '-vf', vf, '-map', '0:v', '-map', '[a]', '-t', f'{d:.3f}',
             '-c:v', 'libx264', '-crf', '14', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', seg])
        segs.append(seg)
        w1, w2 = s['words']; sp = L['split']
        caps.append((w1, t0 + at, t0 + at + sp)); caps.append((w2, t0 + at + sp, min(t0 + at + L['dur'] + 0.35, t0 + d)))
        t0 += d
    total = t0
    with open(f'{TMP}/list.txt', 'w') as f:
        for s in segs: f.write(f"file '{os.path.abspath(s).replace(chr(92), '/')}'\n")
    run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{TMP}/list.txt', '-c', 'copy', f'{TMP}/cut.mov'])

    overlays = [(TITLE[0], TITLE[1], TITLE[2], 60, 215, (255, 225, 60, 255))]
    overlays += [(t, a, b, 118, 1330, (255, 255, 255, 255)) for t, a, b in caps]
    overlays += [(END[0], total - END[1], total, 150, 560, (255, 225, 60, 255))]
    inputs, fc, last = [], [], '0:v'
    for i, (txt, a, b, size, y, col) in enumerate(overlays):
        p = f'{TMP}/cap{i}.png'; text_png(p, txt, size, y, col); inputs += ['-i', p]
        fc.append(f"[{last}][{i + 1}:v]overlay=enable='between(t,{a:.2f},{b:.2f})'[v{i}]"); last = f'v{i}'
    fc.append(f"anoisesrc=color=brown:amplitude=0.012:duration={total:.2f}:sample_rate=48000,lowpass=f=900,pan=stereo|c0=c0|c1=c0[bed]")
    fc.append(f"[0:a][bed]amix=inputs=2:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=11,afade=t=out:st={total - 0.25:.2f}:d=0.25[a]")
    out = f'{OUT}/{NAME}.mp4'
    run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{TMP}/cut.mov'] + inputs + ['-filter_complex', ';'.join(fc), '-map', f'[{last}]', '-map', '[a]',
         '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
         '-movflags', '+faststart', '-t', f'{total:.2f}', out])
    run(['ffmpeg', '-y', '-loglevel', 'error', '-i', out, '-vf', f'fps=1,scale=216:-1,tile={int(total) + 1}x1', '-frames:v', '1', f'{OUT}/{NAME}_sheet.jpg'])
    print('ok', out, f'{total:.2f}s'); print([(t, round(a, 2), round(b, 2)) for t, a, b in caps if t.isascii()])

if __name__ == '__main__':
    main()

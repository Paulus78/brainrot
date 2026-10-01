"""Schnitt von Folge 9 "Bongo brainrot" (Banga operiert Bongos verschimmeltes Gehirn).
Bild: Flow-Clips mit Start-/Endbild (clips). Stimmen: je EINE Aufnahme pro Figur (voice/bongo2, voice/banga2),
in Zeilen geschnitten und an den Sprechstellen ueber den Clip gelegt; Originalton dort stumm. Keine Untertitel.
Aufruf (im Repo-Ordner): python episodes/ep009_bongo_brainrot/edit.py"""
import os, subprocess, sys
sys.path.insert(0, 'tools')
from sync import align

EP = 'episodes/ep009_bongo_brainrot'; CL = f'{EP}/clips'; TMP = f'{EP}/tmp'; OUT = 'output/ep009'
W, H, FPS = 1080, 1920, 30
NAME = 'bongo_ep009_v2'
VOICES = {'bongo': (f'{EP}/voice/bongo2', 4, 1.5), 'banga': (f'{EP}/voice/banga2', 2, 1.5)}   # Ordner, Halbtoene, Lautstaerke

# dubs: (Figur, Zeile, Suchfenster von, bis) - die genaue Stelle findet tools/sync.py am Originalton (lippensynchron)
SHOTS = [
    dict(clip='S1b', cut=(0.50, 6.50), dubs=[('bongo', 1, 1.80, 5.40)]),                                  # Bongo headache.
    dict(clip='S2a', cut=(0.00, 8.50), dubs=[('banga', 1, 0.00, 4.00)]),                                  # Banga doctor.
    dict(clip='S3a', cut=(0.30, 9.90), dubs=[('banga', 2, 7.20, 10.0)]),                                  # Banga... eww.
    dict(clip='S4a', cut=(0.30, 9.60), dubs=[('bongo', 2, 5.80, 10.0)]),                                  # Bongo quantum physics.
    dict(clip='S5b', cut=(0.00, 9.60), dubs=[('banga', 3, 0.00, 3.50)]),                                  # Banga boring.
    dict(clip='S6a', cut=(0.30, 10.0), dubs=[('bongo', 3, 4.60, 7.20), ('banga', 4, 6.60, 8.60), ('banga', 5, 8.00, 10.0)]),  # Bongo banana. / Banga fixa. / Banga perfecta.
]

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: raise SystemExit(r.stderr[-1500:])

def main():
    os.makedirs(TMP, exist_ok=True); os.makedirs(OUT, exist_ok=True)
    segs, t0, marks = [], 0.0, []
    for si, s in enumerate(SHOTS):
        a, b = s['cut']; d = b - a; seg = f'{TMP}/s{si}.mov'; fade = 0.06
        vf = f'setpts=PTS-STARTPTS,fps={FPS},scale={W}:{H}:flags=lanczos,unsharp=5:5:0.5'
        # Originalton: in jedem Stumm-Fenster weich auf 0
        gain = '1'
        placed = []
        for who, line, w0, w1 in s['dubs']:
            folder, semis, vol = VOICES[who]
            at, st, q = align(f'{CL}/{s["clip"]}.mp4', w0, w1, f'{folder}/line_{line}.wav', semis)
            placed.append((who, line, at, st)); print(f'  {s["clip"]} {who} {line}: Start {at:.2f}s, Dehnung {st:.2f}, Guete {q:.2f}')
        for who, line, w0, w1 in s['dubs']:
            m0, m1 = max(w0, a) - a, min(w1, b) - a
            gain = (f"if(between(t,{m0:.3f},{m1:.3f}),0,if(between(t,{m0 - fade:.3f},{m0:.3f}),({m0:.3f}-t)/{fade},"
                    f"if(between(t,{m1:.3f},{m1 + fade:.3f}),(t-{m1:.3f})/{fade},{gain})))")
        fc = [f"[0:a]asetpts=PTS-STARTPTS,aresample=48000,volume='{gain}':eval=frame,afade=t=in:d=0.03,afade=t=out:st={d - 0.05:.3f}:d=0.05,volume=0.9[sfx]"]
        ins, mix = [], '[sfx]'
        n = 0
        for who, line, at, st in placed:
            folder, semis, vol = VOICES[who]; r = 2 ** (semis / 12)
            fx = f',atempo={1 / st:.4f}'
            ins += ['-i', f'{folder}/line_{line}.wav']
            fc.append(f"[{n + 1}:a]asetrate={int(48000 * r)},aresample=48000,atempo={1 / r:.5f}{fx},adelay={int((at - a) * 1000)}:all=1,volume={vol}[vo{n}]")
            mix += f'[vo{n}]'; marks.append((who, line, round(t0 + at - a, 2))); n += 1
        fc.append(f"{mix}amix=inputs={n + 1}:normalize=0:duration=first,pan=stereo|c0=c0|c1=c0[a]")
        run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(a), '-to', str(b), '-i', f'{CL}/{s["clip"]}.mp4'] + ins +
            ['-filter_complex', ';'.join(fc), '-vf', vf, '-map', '0:v', '-map', '[a]', '-t', f'{d:.3f}',
             '-c:v', 'libx264', '-crf', '14', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', seg])
        segs.append(seg); t0 += d
    total = t0
    with open(f'{TMP}/list.txt', 'w') as f:
        for s in segs: f.write("file '" + os.path.abspath(s).replace(chr(92), '/') + "'" + chr(10))
    run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{TMP}/list.txt', '-c', 'copy', f'{TMP}/cut.mov'])
    fc = (f"anoisesrc=color=brown:amplitude=0.010:duration={total:.2f}:sample_rate=48000,lowpass=f=900,pan=stereo|c0=c0|c1=c0[bed];"
          f"[0:a][bed]amix=inputs=2:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=11,afade=t=out:st={total - 0.3:.2f}:d=0.3[a]")
    out = f'{OUT}/{NAME}.mp4'
    run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{TMP}/cut.mov', '-filter_complex', fc, '-map', '0:v', '-map', '[a]',
         '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
         '-movflags', '+faststart', '-t', f'{total:.2f}', out])
    print('ok', out, f'{total:.2f}s', 'Zeilen bei', marks)

if __name__ == '__main__':
    main()

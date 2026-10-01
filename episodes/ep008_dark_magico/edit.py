"""Schnitt von Folge 8 "Banga dark magico" (Zauberstab-Story: Bongo zaubert Gutes aus dem Eimer, Banga verflucht ihn).
Bild: Flow-Clips mit Start-/Endbild (clips). Stimmen: je EINE Aufnahme pro Figur (voice/bongo2, voice/banga2),
in Zeilen geschnitten und an den Sprechstellen ueber den Clip gelegt; Originalton dort stumm. Keine Untertitel.
Aufruf (im Repo-Ordner): python episodes/ep008_dark_magico/edit.py"""
import os, subprocess

EP = 'episodes/ep008_dark_magico'; CL = f'{EP}/clips'; TMP = f'{EP}/tmp'; OUT = 'output/ep008'
W, H, FPS = 1080, 1920, 30
NAME = 'bongo_ep008_v1'
VOICES = {'bongo': (f'{EP}/voice/bongo2', 4, 1.5), 'banga': (f'{EP}/voice/banga2', 2, 1.5)}   # Ordner, Halbtoene, Lautstaerke

# dubs: (Figur, Zeile, Startzeit im Clip, stumm von, stumm bis[, 'muffle' = dumpf, wie aus dem Bauch der Schlange])
SHOTS = [
    dict(clip='S1b', cut=(0.80, 6.00), dubs=[('bongo', 1, 1.40, 1.10, 4.80)]),                                   # Bongo magico!
    dict(clip='S2a', cut=(1.20, 8.15), dubs=[('bongo', 2, 6.60, 6.40, 8.15), ('bongo', 0, 0, 1.80, 3.00)]),       # Bongo delicioso.
    dict(clip='S3b', cut=(1.60, 8.00), dubs=[('banga', 1, 3.65, 3.40, 4.80), ('bongo', 3, 5.85, 5.60, 7.20)]),    # Banga want. / Bongo no share.
    dict(clip='S4a', cut=(1.40, 9.20), dubs=[('banga', 2, 1.90, 1.40, 3.50)]),                                   # Banga dark magico!
    dict(clip='S5b', cut=(1.50, 9.00), dubs=[('bongo', 4, 5.60, 5.40, 7.50)]),                                   # Bongo... uh oh.
    dict(clip='S6b', cut=(0.00, 9.00), dubs=[('bongo', 5, 5.55, 5.30, 6.60, 'muffle'), ('banga', 3, 7.15, 6.90, 8.40)]),  # Bongo dead. / Banga yummy.
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
        for dub in s['dubs']:
            m0, m1 = dub[3] - a, dub[4] - a
            gain = (f"if(between(t,{m0:.3f},{m1:.3f}),0,if(between(t,{m0 - fade:.3f},{m0:.3f}),({m0:.3f}-t)/{fade},"
                    f"if(between(t,{m1:.3f},{m1 + fade:.3f}),(t-{m1:.3f})/{fade},{gain})))")
        fc = [f"[0:a]asetpts=PTS-STARTPTS,aresample=48000,volume='{gain}':eval=frame,afade=t=in:d=0.03,afade=t=out:st={d - 0.05:.3f}:d=0.05,volume=0.9[sfx]"]
        ins, mix = [], '[sfx]'
        n = 0
        for dub in s['dubs']:
            who, line, at = dub[:3]
            if not line: continue                      # Zeile 0 = nur stummschalten
            folder, semis, vol = VOICES[who]; r = 2 ** (semis / 12)
            fx = ',lowpass=f=650,volume=1.6' if len(dub) > 5 and dub[5] == 'muffle' else ''
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

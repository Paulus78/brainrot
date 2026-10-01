"""Gemeinsamer Schnitt fuer alle Folgen: Clips schneiden, Stimmzeilen lippensynchron einsetzen (tools/sync.py),
Originalton an den Sprechstellen stummschalten, Lautheit angleichen, 1080x1920 ausgeben.

SHOTS-Eintrag: dict(clip='S1a', cut=(von, bis), dubs=[(Figur, Zeile, Suchfenster_von, Suchfenster_bis[, 'muffle'])], mute=[(von, bis)])
VOICES: {Figur: (Ordner mit line_N.wav, Halbtoene, Lautstaerke)}"""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sync import align

W, H, FPS = 1080, 1920, 30

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: raise SystemExit(r.stderr[-1500:])

def build(ep, out_dir, name, voices, shots):
    cl, tmp = f'{ep}/clips', f'{ep}/tmp'
    os.makedirs(tmp, exist_ok=True); os.makedirs(out_dir, exist_ok=True)
    segs, t0 = [], 0.0
    for si, s in enumerate(shots):
        a, b = s['cut']; d = b - a; seg = f'{tmp}/s{si}.mov'; fade = 0.06
        clip = f'{cl}/{s["clip"]}.mp4'
        placed, mutes = [], list(s.get('mute', []))
        for dub in s.get('dubs', []):
            who, line, w0, w1 = dub[:4]; folder, semis, vol = voices[who]
            at, st, q = align(clip, w0, w1, f'{folder}/line_{line}.wav', semis)
            placed.append((who, line, at, st, dub[4] if len(dub) > 4 else ''))
            mutes.append((w0, w1))
            print(f'  {s["clip"]} {who} {line}: Start {at:.2f}s, Dehnung {st:.2f}, Guete {q:.2f}' + ('   <-- unsicher' if q < 0.6 else ''))
        gain = '1'
        for m0, m1 in mutes:
            m0, m1 = max(m0, a) - a, min(m1, b) - a
            gain = (f"if(between(t,{m0:.3f},{m1:.3f}),0,if(between(t,{m0 - fade:.3f},{m0:.3f}),({m0:.3f}-t)/{fade},"
                    f"if(between(t,{m1:.3f},{m1 + fade:.3f}),(t-{m1:.3f})/{fade},{gain})))")
        fc = [f"[0:a]asetpts=PTS-STARTPTS,aresample=48000,volume='{gain}':eval=frame,afade=t=in:d=0.03,afade=t=out:st={d - 0.05:.3f}:d=0.05,volume=0.9[sfx]"]
        ins, mix = [], '[sfx]'
        for n, (who, line, at, st, opt) in enumerate(placed):
            folder, semis, vol = voices[who]; r = 2 ** (semis / 12)
            fx = f',atempo={1 / st:.4f}' + (',lowpass=f=650,volume=1.6' if opt == 'muffle' else '')
            ins += ['-i', f'{folder}/line_{line}.wav']
            fc.append(f"[{n + 1}:a]asetrate={int(48000 * r)},aresample=48000,atempo={1 / r:.5f}{fx},adelay={int(max(at - a, 0) * 1000)}:all=1,volume={vol}[vo{n}]")
            mix += f'[vo{n}]'
        fc.append(f"{mix}amix=inputs={len(placed) + 1}:normalize=0:duration=first,pan=stereo|c0=c0|c1=c0[a]")
        vf = f'setpts=PTS-STARTPTS,fps={FPS},scale={W}:{H}:flags=lanczos,unsharp=5:5:0.5'
        run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(a), '-to', str(b), '-i', clip] + ins +
            ['-filter_complex', ';'.join(fc), '-vf', vf, '-map', '0:v', '-map', '[a]', '-t', f'{d:.3f}',
             '-c:v', 'libx264', '-crf', '14', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', seg])
        segs.append(seg); t0 += d
    with open(f'{tmp}/list.txt', 'w') as f:
        for s in segs: f.write("file '" + os.path.abspath(s).replace(chr(92), '/') + "'" + chr(10))
    run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{tmp}/list.txt', '-c', 'copy', f'{tmp}/cut.mov'])
    fc = (f"anoisesrc=color=brown:amplitude=0.010:duration={t0:.2f}:sample_rate=48000,lowpass=f=900,pan=stereo|c0=c0|c1=c0[bed];"
          f"[0:a][bed]amix=inputs=2:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=11,afade=t=out:st={t0 - 0.3:.2f}:d=0.3[a]")
    out = f'{out_dir}/{name}.mp4'
    run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{tmp}/cut.mov', '-filter_complex', fc, '-map', '0:v', '-map', '[a]',
         '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
         '-movflags', '+faststart', '-t', f'{t0:.2f}', out])
    print('ok', out, f'{t0:.2f}s')

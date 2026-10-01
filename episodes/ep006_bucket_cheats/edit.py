"""Schnitt von Folge 6 "Eimer geht fremd".
Bild: Flow-Clips mit Start- und Endbild (clips). Stimme: fuenf Zeilen aus EINER Aufnahme (voice/t1/line_N.wav),
um PITCH Halbtoene angehoben (heller), an der Sprechstelle ueber den Clip gelegt; Originalton dort stumm.
Keine Untertitel. Aufruf (im Repo-Ordner): python episodes/ep006_bucket_cheats/edit.py"""
import os, json, subprocess

EP = 'episodes/ep006_bucket_cheats'; CL = f'{EP}/clips'; VO = f'{EP}/voice/t1'; TMP = f'{EP}/tmp'; OUT = 'output/ep006'
W, H, FPS = 1080, 1920, 30
NAME = 'bongo_ep006_v1'
PITCH = 4            # Halbtoene heller (Stimmtest-Variante B)

# clip, Schnitt (von, bis), stumm (von, bis) im Clip, Zeile + Startzeit im Clip
SHOTS = [
    dict(clip='S1a', cut=(1.60, 7.20), mute=(4.75, 7.20), line=1, at=5.25),   # "Bongo... bucketo?!"
    dict(clip='S2a', cut=(0.30, 6.00), mute=(2.20, 6.00), line=2, at=3.60),   # "Bongo bucketo!"
    dict(clip='S3b', cut=(0.80, 8.00), mute=(6.30, 8.00), line=3, at=6.55),   # "Bongo... no."
    dict(clip='S4a', cut=(1.20, 7.00), mute=(5.30, 7.00), line=4, at=5.45),   # "Bongo new bucketo."
    dict(clip='S5a', cut=(0.90, 6.20), mute=None, line=None, at=None),         # Katze springt um
    dict(clip='S6a', cut=(1.20, 7.60), mute=(4.20, 7.60), line=5, at=5.10),   # "Bongo fixo."
]

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: raise SystemExit(r.stderr[-1500:])

def main():
    os.makedirs(TMP, exist_ok=True); os.makedirs(OUT, exist_ok=True)
    segs, t0, marks = [], 0.0, []
    r = 2 ** (PITCH / 12)
    for si, s in enumerate(SHOTS):
        a, b = s['cut']; d = b - a; seg = f'{TMP}/s{si}.mov'
        vf = f'setpts=PTS-STARTPTS,fps={FPS},scale={W}:{H}:flags=lanczos,unsharp=5:5:0.5'
        base = f"[0:a]asetpts=PTS-STARTPTS,aresample=48000"
        tail = f"afade=t=in:d=0.03,afade=t=out:st={d - 0.05:.3f}:d=0.05,volume=0.9"
        if s['line']:
            m0, m1 = s['mute'][0] - a, s['mute'][1] - a; at = s['at'] - a; fade = 0.06
            vol = (f"volume='if(between(t,{m0:.3f},{m1:.3f}),0,if(between(t,{m0 - fade:.3f},{m0:.3f}),({m0:.3f}-t)/{fade},"
                   f"if(between(t,{m1:.3f},{m1 + fade:.3f}),(t-{m1:.3f})/{fade},1)))':eval=frame")
            fc = (f"{base},{vol},{tail}[sfx];"
                  f"[1:a]asetrate={int(48000 * r)},aresample=48000,atempo={1 / r:.5f},adelay={int(at * 1000)}:all=1,volume=1.5[vo];"
                  f"[sfx][vo]amix=inputs=2:normalize=0:duration=first,pan=stereo|c0=c0|c1=c0[a]")
            ins = ['-i', f'{VO}/line_{s["line"]}.wav']; marks.append((s['line'], round(t0 + at, 2)))
        else:
            fc = f"{base},{tail},pan=stereo|c0=c0|c1=c0[a]"; ins = []
        run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(a), '-to', str(b), '-i', f'{CL}/{s["clip"]}.mp4'] + ins +
            ['-filter_complex', fc, '-vf', vf, '-map', '0:v', '-map', '[a]', '-t', f'{d:.3f}',
             '-c:v', 'libx264', '-crf', '14', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', seg])
        segs.append(seg); t0 += d
    total = t0
    with open(f'{TMP}/list.txt', 'w') as f:
        for s in segs: f.write(f"file '{os.path.abspath(s).replace(chr(92), '/')}'" + chr(10))
    run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{TMP}/list.txt', '-c', 'copy', f'{TMP}/cut.mov'])
    fc = (f"anoisesrc=color=brown:amplitude=0.012:duration={total:.2f}:sample_rate=48000,lowpass=f=900,pan=stereo|c0=c0|c1=c0[bed];"
          f"[0:a][bed]amix=inputs=2:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=11,afade=t=out:st={total - 0.3:.2f}:d=0.3[a]")
    out = f'{OUT}/{NAME}.mp4'
    run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{TMP}/cut.mov', '-filter_complex', fc, '-map', '0:v', '-map', '[a]',
         '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
         '-movflags', '+faststart', '-t', f'{total:.2f}', out])
    run(['ffmpeg', '-y', '-loglevel', 'error', '-i', out, '-vf', f'fps=1,scale=216:-1,tile={int(total) + 1}x1', '-frames:v', '1', f'{OUT}/{NAME}_sheet.jpg'])
    print('ok', out, f'{total:.2f}s', 'Zeilen bei', marks)

if __name__ == '__main__':
    main()

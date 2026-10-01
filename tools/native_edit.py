"""Schnitt mit dem ORIGINALTON der Clips (Stimme kommt direkt aus Flow -> kostenlos und lippensynchron).
Damit die Stimmen ueber die Clips gleich klingen, wird die Tonhoehe nur an den Sprechstellen angeglichen.

SHOTS-Eintrag: dict(clip='T1', cut=(von, bis), pitch=[(von, bis, Halbtoene), ...])   Zeiten in Clip-Sekunden"""
import os, subprocess

W, H, FPS = 1080, 1920, 30

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: raise SystemExit(r.stderr[-1500:])

def build(ep, out_dir, name, shots):
    cl, tmp = f'{ep}/clips', f'{ep}/tmp'
    os.makedirs(tmp, exist_ok=True); os.makedirs(out_dir, exist_ok=True)
    segs, total = [], 0.0
    for si, s in enumerate(shots):
        a, b = s['cut']; d = b - a; seg = f'{tmp}/s{si}.mov'
        # Tonspur in Stuecke teilen: unveraendert / Tonhoehe verschoben / unveraendert ...
        marks, parts, pos = sorted(s.get('pitch', [])), [], a
        for p0, p1, semis in marks:
            p0, p1 = max(p0, a), min(p1, b)
            if p0 > pos: parts.append((pos, p0, 0))
            parts.append((p0, p1, semis)); pos = p1
        if pos < b: parts.append((pos, b, 0))
        fc, labels = [], ''
        for i, (p0, p1, semis) in enumerate(parts):
            r = 2 ** (semis / 12)
            shift = f',asetrate={int(48000 * r)},aresample=48000,atempo={1 / r:.5f}' if semis else ''
            fc.append(f'[0:a]atrim={p0:.3f}:{p1:.3f},asetpts=PTS-STARTPTS,aresample=48000{shift}[p{i}]'); labels += f'[p{i}]'
        fc.append(f'{labels}concat=n={len(parts)}:v=0:a=1,afade=t=in:d=0.03,afade=t=out:st={d - 0.05:.3f}:d=0.05,pan=stereo|c0=c0|c1=c0[a]')
        fc.append(f'[0:v]trim={a:.3f}:{b:.3f},setpts=PTS-STARTPTS,fps={FPS},scale={W}:{H}:flags=lanczos,unsharp=5:5:0.5[v]')
        run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{cl}/{s["clip"]}.mp4', '-filter_complex', ';'.join(fc), '-map', '[v]', '-map', '[a]', '-t', f'{d:.3f}',
             '-c:v', 'libx264', '-crf', '14', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'pcm_s16le', seg])
        segs.append(seg); total += d
    with open(f'{tmp}/list.txt', 'w') as f:
        for s in segs: f.write("file '" + os.path.abspath(s).replace(chr(92), '/') + "'" + chr(10))
    run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{tmp}/list.txt', '-c', 'copy', f'{tmp}/cut.mov'])
    out = f'{out_dir}/{name}.mp4'
    run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{tmp}/cut.mov', '-af', f'loudnorm=I=-15:TP=-1.5:LRA=11,afade=t=out:st={total - 0.3:.2f}:d=0.3',
         '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
         '-movflags', '+faststart', '-t', f'{total:.2f}', out])
    print('ok', out, f'{total:.2f}s')

if __name__ == '__main__':
    # Folge 11 "Bongo... rich."
    build('episodes/ep011_bongo_rich', 'output/ep011', 'bongo_ep011_v2', [
        dict(clip='T1b', cut=(0.00, 6.80), pitch=[(0.05, 1.40, 3)]),                      # Banga bye bye. 380 Hz -> ~452 / Bongo bitch. 331 Hz
        dict(clip='T2', cut=(0.00, 7.80)),                                                # Bongo... nothing. 320 Hz
        dict(clip='T3', cut=(0.30, 6.20), pitch=[(4.10, 5.90, 1)]),                       # Bongo CEO.       298 Hz -> ~316
        dict(clip='T4', cut=(0.00, 8.00), pitch=[(0.10, 1.60, -2), (3.50, 4.35, 6)]),     # Banga sorry! 507 -> ~452 / Bongo busy. 176 -> ~250
    ])

"""Ruhige Testszene (Kueche): Bongo + Eimer aus den Flow-Teilen.
Aufruf: python src/flowrig/scene_test.py [voice.wav]  ->  output/flowtest/bongo_flowtest_v1.mp4"""
import os, sys, subprocess, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, DUR = 1080, 1920, 30, 7.6
RIG = 'gen/rig'; OUT = 'output/flowtest'
FACES = ['neutral', 'blink', 'talk', 'talk2', 'shock', 'shout', 'sus', 'smug']

def ease(x):
    x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)

def load_sprite(name):
    im = cv2.imread(f'{RIG}/{name}.png', -1).astype(np.float32)
    a = (im[..., 3] > 40).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(a)           # Randkruemel entfernen
    big = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    keep = cv2.dilate((lab == big).astype(np.uint8), np.ones((9, 9), np.uint8))
    im[..., 3] *= keep
    im[..., :3] *= im[..., 3:4] / 255                              # vormultipliziert
    return im

def place(canvas, spr, anchor, pos, sx, sy, rot=0.0):
    """Sprite so auf die Leinwand legen, dass 'anchor' (Sprite-Pixel) auf 'pos' landet."""
    c, s = np.cos(rot), np.sin(rot)
    M = np.array([[sx * c, -sy * s, 0], [sx * s, sy * c, 0]], np.float32)
    M[:, 2] = np.array(pos) - M[:, :2] @ np.array(anchor)
    w = cv2.warpAffine(spr, M, (W, H), flags=cv2.INTER_LINEAR, borderValue=0)
    a = w[..., 3:4] / 255
    canvas *= (1 - a); canvas += w[..., :3]

def shadow(canvas, cx, cy, rx, ry, strength):
    m = np.zeros((H, W), np.float32)
    cv2.ellipse(m, (int(cx), int(cy)), (int(rx), int(ry)), 0, 0, 360, 1, -1)
    m = cv2.GaussianBlur(m, (0, 0), max(6, ry * 0.45)) * strength
    canvas *= (1 - m[..., None])

# ---------------------------------------------------------------- Ablauf
# (Start, Ende, Gesicht) – spaetere Eintraege ueberschreiben fruehere
FACE_TL = [
    (0.00, 9.00, 'neutral'), (0.70, 0.82, 'blink'),
    (1.30, 2.25, 'sus'),
    (2.30, 2.44, 'talk'), (2.52, 2.66, 'talk2'),                      # Bon-go
    (2.95, 3.07, 'talk'), (3.12, 3.24, 'talk2'), (3.29, 3.44, 'talk'),  # bu-cke-to
    (3.44, 3.95, 'sus'),
    (3.95, 5.05, 'shock'),
    (5.05, 5.22, 'talk'), (5.28, 5.42, 'talk2'),                      # Bon-go
    (5.55, 5.80, 'shout'), (5.80, 5.90, 'talk'), (5.90, 6.25, 'shout'),  # ban-ga ban-ga
    (6.35, 9.00, 'smug'), (7.00, 7.12, 'blink'),
]
CAPS = [(2.30, 2.90, 'BONGO…'), (2.95, 3.80, 'BUCKETO.'), (5.05, 5.50, 'BONGO'), (5.55, 6.35, 'BANGA BANGA!')]
HOP = (3.55, 3.95)      # Eimer huepft
POP = [3.95, 5.55, 5.90]  # kurze Streck-Impulse bei Reaktion / Rufen

def face_at(t):
    f = 'neutral'
    for a, b, n in FACE_TL:
        if a <= t < b: f = n
    return f

def pop(t):
    v = 0.0
    for p in POP:
        d = t - p
        if 0 <= d < 0.35: v += np.exp(-d * 11) * np.cos(d * 22) * 0.045
    return v

def caption(text):
    font = ImageFont.truetype('C:/Windows/Fonts/ariblk.ttf', 96)
    im = Image.new('RGBA', (W, 220), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    w = d.textlength(text, font=font)
    d.text(((W - w) / 2, 40), text, font=font, fill=(255, 255, 255, 255), stroke_width=9, stroke_fill=(20, 20, 20, 255))
    a = np.asarray(im).astype(np.float32)
    return a[..., [2, 1, 0]] * a[..., 3:4] / 255, a[..., 3:4] / 255

def main():
    os.makedirs(OUT, exist_ok=True)
    voice = sys.argv[1] if len(sys.argv) > 1 else None
    out = f'{OUT}/bongo_flowtest_v1.mp4'
    bg = cv2.imread(f'{RIG}/kitchen.png')
    s = max(W / bg.shape[1], H / bg.shape[0])
    bg = cv2.resize(bg, None, fx=s, fy=s, interpolation=cv2.INTER_CUBIC)
    y0 = (bg.shape[0] - H) // 2; x0 = (bg.shape[1] - W) // 2
    bg = cv2.GaussianBlur(bg[y0:y0 + H, x0:x0 + W], (0, 0), 2.2).astype(np.float32) * 0.93
    faces = {n: load_sprite(f'face_{n}') for n in FACES}
    bucket = load_sprite('bucket')
    caps = {c[2]: caption(c[2]) for c in CAPS}
    ys, xs = np.where(faces['neutral'][..., 3] > 40)
    anchor = ((xs.min() + xs.max()) / 2, ys.max() - 6)          # Fusspunkt
    BONGO = (650, 1560); BSC = 1.12
    BK = (235, 1585); KSC = 0.40

    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-']
    if voice: cmd += ['-i', voice]
    cmd += ['-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'medium']
    cmd += (['-c:a', 'aac', '-b:a', '192k', '-shortest'] if voice else ['-an']) + [out]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    stills = {}
    for i in range(int(DUR * FPS)):
        t = i / FPS
        fr = bg.copy()
        # langsamer Push-in (insgesamt ~4 %), sonst steht die Kamera
        z = 1 + 0.04 * ease(t / DUR)
        # Eimer
        h = 0.0; ksx = ksy = 1.0
        if HOP[0] <= t < HOP[1]:
            u = (t - HOP[0]) / (HOP[1] - HOP[0]); h = 70 * 4 * u * (1 - u)
        d = t - HOP[1]
        if 0 <= d < 0.25: ksy = 1 - 0.07 * np.exp(-d * 14) * np.cos(d * 30); ksx = 2 - ksy
        shadow(fr, BK[0], BK[1] - 8, 150 - h * 0.4, 30, 0.42 - h * 0.002); shadow(fr, BK[0], BK[1] - 10, 105 - h * 0.4, 16, 0.5 - h * 0.006)
        place(fr, bucket, (bucket.shape[1] / 2, bucket.shape[0] - 4), (BK[0], BK[1] - h), KSC * ksx, KSC * ksy)
        # Bongo: Atmen + kurze Impulse, sonst ruhig
        br = 0.007 * np.sin(2 * np.pi * t / 3.4)
        p = pop(t)
        sy = BSC * (1 + br + p); sx = BSC * (1 - br * 0.5 - p * 0.6)
        shadow(fr, BONGO[0] - 10, BONGO[1] - 4, 270, 50, 0.50)
        shadow(fr, BONGO[0] - 95, BONGO[1] - 14, 105, 20, 0.45); shadow(fr, BONGO[0] + 95, BONGO[1] - 22, 80, 16, 0.45)
        place(fr, faces[face_at(t)], anchor, BONGO, sx, sy)
        # Untertitel
        for a, b, txt in CAPS:
            if a <= t < b:
                c, al = caps[txt]; k = 1 + 0.10 * np.exp(-(t - a) * 16)
                ch, cw = c.shape[:2]
                c2 = cv2.resize(c, None, fx=k, fy=k); a2 = cv2.resize(al, None, fx=k, fy=k)[..., None]
                oy = (c2.shape[0] - ch) // 2; ox = (c2.shape[1] - cw) // 2
                c2 = c2[oy:oy + ch, ox:ox + cw]; a2 = a2[oy:oy + ch, ox:ox + cw]
                reg = fr[1640:1640 + ch]; reg *= (1 - a2); reg += c2
        if z != 1:
            M = cv2.getRotationMatrix2D((W / 2, 1150), 0, z)
            fr = cv2.warpAffine(fr, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        f8 = np.clip(fr, 0, 255).astype(np.uint8)
        ff.stdin.write(f8.tobytes())
        if i in (15, 22, 50, 70, 95, 112, 130, 170, 180, 215): stills[i] = cv2.resize(f8, (432, 768))
    ff.stdin.close(); ff.wait()
    cv2.imwrite(f'{OUT}/bongo_flowtest_v1_sheet.jpg', np.hstack([stills[k] for k in sorted(stills)]))
    print('ok', out)

if __name__ == '__main__':
    main()

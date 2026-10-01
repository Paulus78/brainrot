"""Baut aus den Flow-Bildern (gen/inbox) saubere Rig-Teile (gen/rig):
Koerper ohne Arme, zwei Arme, Gesichts-Varianten (deckungsgleich), Eimer, Kueche."""
import os, numpy as np, cv2
IN = 'gen/inbox'; OUT = 'gen/rig'
MASTER, ARMLESS = 19, 16
FACES = {'neutral': 19, 'blink': 15, 'talk': 6, 'talk2': 13, 'shock': 12, 'shout': 4,
         'sus': 9, 'smug': 10}

def load(k):
    return cv2.imread(f'{IN}/flow_{k:02d}.jpg').astype(np.float32)  # BGR

def key(img, fur_fix=True):
    """Gruen freistellen: alpha aus 'wie viel gruener als rot/blau', dann Gruenstich entfernen."""
    b, g, r = img[..., 0], img[..., 1], img[..., 2]
    green = g - np.maximum(r, b)
    a = 1 - np.clip((green - 8) / 55, 0, 1)
    a = cv2.GaussianBlur(a, (0, 0), 0.8)
    a = np.clip((a - 0.45) / 0.5, 0, 1)
    out = img.copy(); out[..., 1] = np.minimum(g, np.maximum(r, b))
    # Randpixel: Gelbgruen-Saum Richtung Fellfarbe ziehen (gruen an rot koppeln)
    # Gruenstich am Rand (Reflex vom Greenscreen) Richtung Fellfarbe ziehen.
    # Nur in einem Band entlang der Silhouette; Weiss/Blau (b hoch) und Banane (hell-gelb) bleiben.
    inner = cv2.erode((a > 0.5).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (45, 45)))
    band = cv2.GaussianBlur(1 - inner.astype(np.float32), (0, 0), 6)
    band = np.maximum(band, 0.75)            # innen abgeschwaecht, am Rand voll
    band[:300] = np.minimum(band[:300], cv2.GaussianBlur(1 - inner.astype(np.float32), (0, 0), 6)[:300])
    if not fur_fix: band[:] = 0
    fur = (b < 0.6 * r) & ~((r > 195) & (g > 160))
    lim = r * 0.70 + b * 0.12
    g2 = np.where(fur, np.minimum(out[..., 1], lim), out[..., 1])
    out[..., 1] = out[..., 1] * (1 - band) + g2 * band
    return np.dstack([out, a * 255])

def save(name, rgba):
    cv2.imwrite(f'{OUT}/{name}.png', np.clip(rgba, 0, 255).astype(np.uint8))

def soft(mask, grow, feather):
    m = cv2.dilate(mask.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (grow, grow)))
    return cv2.GaussianBlur(m.astype(np.float32), (0, 0), feather)

def main():
    os.makedirs(OUT, exist_ok=True)
    m_raw, a_raw = load(MASTER), load(ARMLESS)
    master, base = key(m_raw), key(a_raw)
    H, W = base.shape[:2]
    # --- Arme: dort, wo Master und armlose Variante stark abweichen (nur Rumpfhoehe)
    d = cv2.GaussianBlur(np.abs(m_raw - a_raw).sum(2), (0, 0), 2)
    ma, ba = master[..., 3] / 255, base[..., 3] / 255
    outside = ((ma > 0.5) & (ba < 0.5)).astype(np.uint8); outside[:850] = 0; outside[1040:] = 0
    outside = cv2.morphologyEx(outside, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    near = cv2.dilate(outside, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (61, 61)))
    lum = cv2.GaussianBlur(m_raw.mean(2), (0, 0), 1.5)
    am = ((outside > 0) | ((near > 0) & (d > 45) & (lum > 95))).astype(np.uint8)
    am = cv2.morphologyEx(am, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))
    am = cv2.morphologyEx(am, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
    n, lab, st, _ = cv2.connectedComponentsWithStats(am)
    comps = sorted(range(1, n), key=lambda i: -st[i, cv2.CC_STAT_AREA])[:2]
    comps.sort(key=lambda i: st[i, cv2.CC_STAT_LEFT])
    meta = {}
    for nm, ci in zip(['arm_l', 'arm_r'], comps):  # l = links im Bild
        m = cv2.GaussianBlur((lab == ci).astype(np.float32), (0, 0), 2.0) * ma
        arm = master.copy(); arm[..., 3] = np.clip(m, 0, 1) * 255
        x, y, w, h = st[ci, :4]; p = 14
        x0, y0, x1, y1 = max(x - p, 0), max(y - p, 0), min(x + w + p, W), min(y + h + p, H)
        save(nm, arm[y0:y1, x0:x1]); meta[nm] = [int(x0), int(y0), int(x1), int(y1)]
    save('body', base)
    # --- Gesichter: nur der Bereich, der sich gegenueber dem Master wirklich aendert
    for nm, k in FACES.items():
        v_raw = load(k); v = key(v_raw)
        dd = cv2.GaussianBlur(np.abs(v_raw - m_raw).sum(2), (0, 0), 4)
        fm = (dd > 60); fm[840:] = False   # nur Kopf
        m = np.clip(soft(fm, 31, 9) * 1.6, 0, 1)
        if nm == 'neutral': m = np.zeros_like(m)
        comp = base.copy()
        # neutral = Master-Kopf auf armlosem Koerper, damit alle Gesichter gleiche Basis haben
        hm = np.zeros((H, W), np.float32); hm[:840] = 1; hm = cv2.GaussianBlur(hm, (0, 0), 12)
        mm = np.maximum(m, hm * 0 )[..., None]
        comp = comp * (1 - mm) + v * mm
        save(f'face_{nm}', comp)
    # --- Eimer
    bk = key(load(3), fur_fix=False); ys, xs = np.where(bk[..., 3] > 20)
    save('bucket', bk[ys.min():ys.max() + 1, xs.min():xs.max() + 1])
    cv2.imwrite(f'{OUT}/kitchen.png', cv2.imread(f'{IN}/flow_00.jpg'))
    import json; json.dump(meta, open(f'{OUT}/meta.json', 'w'))
    # Debug-Blatt auf Grau
    def on_gray(rgba, s=0.5):
        bg = np.full(rgba.shape[:2] + (3,), 120, np.float32); a = rgba[..., 3:4] / 255
        return cv2.resize((rgba[..., :3] * a + bg * (1 - a)).astype(np.uint8), None, fx=s, fy=s)
    row = [on_gray(cv2.imread(f'{OUT}/face_{n}.png', -1).astype(np.float32)) for n in FACES]
    cv2.imwrite('gen/_rig_faces.jpg', np.hstack(row)[150:650])
    arms = np.zeros((H, W, 4), np.float32)
    for nm in meta:
        x0, y0, x1, y1 = meta[nm]; arms[y0:y1, x0:x1] = cv2.imread(f'{OUT}/{nm}.png', -1)
    cv2.imwrite('gen/_rig_arms.jpg', np.hstack([on_gray(base, 1)[820:1300, 150:650], on_gray(arms, 1)[820:1300, 150:650], on_gray(master, 1)[820:1300, 150:650]]))
    print(meta)
main()

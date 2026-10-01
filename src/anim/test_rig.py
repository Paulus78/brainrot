import sys, time
sys.path.insert(0, 'src/anim')
import numpy as np, cv2
from engine import *
import bongo as B

b = B.Bongo()
t0 = time.time()
tiles = []
names = ['neutral','suspicious','annoyed','realization','confident','intense','shocked','pleased','smug']
for n in names:
    canvas = np.full((H, W, 3), (70, 50, 40), np.uint8)
    cam = Cam(cx=540, cy=930, z=1.0)
    pose = B.expr(n)
    b.draw(canvas, cam, dict(pose, x=540, y=1370, s=0.9))
    crop = canvas[330:1500, 60:1020]
    crop = cv2.resize(crop, None, fx=0.42, fy=0.42, interpolation=cv2.INTER_AREA)
    cv2.putText(crop, n, (8, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
    tiles.append(crop)
print('draw time per frame ~', (time.time()-t0)/len(names))
rows = [np.hstack(tiles[i:i+3]) for i in range(0, 9, 3)]
cv2.imwrite('work/expr_sheet.png', np.vstack(rows))
ref = cv2.imread('assets/character_master/bongo_reference.png')
cv2.imwrite('work/neutral_vs_ref.png', np.hstack([cv2.resize(ref,(int(940*0.6),int(1672*0.6))), cv2.resize(tiles[0],None,fx=1.5,fy=1.5)]) if False else cv2.resize(ref,(470,836)))

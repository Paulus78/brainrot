"""Vier Bildvarianten nebeneinander: python tools/quad.py KA  ->  gen/_pair.jpg"""
import sys
from PIL import Image, ImageDraw
k = sys.argv[1]; n = int(sys.argv[2]) if len(sys.argv) > 2 else 4
s = Image.new('RGB', (n * 500, 896))
for i in range(n):
    im = Image.open(f'gen/inbox/{k}_{i}.jpg').resize((500, 896)); s.paste(im, (i * 500, 0)); ImageDraw.Draw(s).text((i * 500 + 8, 8), f'{k}_{i}', fill='white')
s.save('gen/_pair.jpg', quality=85)

"""Zwei Bildvarianten nebeneinander zur Sichtung: python tools/pair.py F1  ->  gen/_pair.jpg"""
import sys
from PIL import Image
k = sys.argv[1]
a = Image.open(f'gen/inbox/{k}_0.jpg'); b = Image.open(f'gen/inbox/{k}_1.jpg')
s = Image.new('RGB', (1116, 1000)); s.paste(a.resize((558, 1000)), (0, 0)); s.paste(b.resize((558, 1000)), (558, 0))
s.save('gen/_pair.jpg', quality=85)

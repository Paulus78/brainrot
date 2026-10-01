"""Lippensynchrone Fassungen der Folgen 6-9. Aufruf (im Repo-Ordner): python tools/edit_all.py [ep006 ep007 ...]
dubs: (Figur, Zeile, Suchfenster von, bis[, 'muffle']) - die genaue Stelle findet tools/sync.py am Originalton."""
import sys
sys.path.insert(0, 'tools')
from episode_edit import build

def ep006():
    EP = 'episodes/ep006_bucket_cheats'
    V = {'bongo': (f'{EP}/voice/t1', 4, 1.5)}
    S = [
        dict(clip='S1a', cut=(1.60, 7.20), dubs=[('bongo', 1, 4.30, 7.20)]),   # Bongo... bucketo?!
        dict(clip='S2a', cut=(0.30, 6.00), dubs=[('bongo', 2, 1.80, 6.00)]),   # Bongo bucketo!
        dict(clip='S3b', cut=(0.80, 8.00), dubs=[('bongo', 3, 5.60, 8.00)]),   # Bongo... no.
        dict(clip='S4a', cut=(1.20, 7.00), dubs=[('bongo', 4, 3.90, 7.00)]),   # Bongo new bucketo.
        dict(clip='S5a', cut=(0.90, 6.20)),
        dict(clip='S6a', cut=(1.20, 7.60), dubs=[('bongo', 5, 4.00, 7.60)]),   # Bongo fixo.
    ]
    build(EP, 'output/ep006', 'bongo_ep006_v2', V, S)

def ep007():
    EP = 'episodes/ep007_banga_or_bucket'
    V = {'bongo': (f'{EP}/voice/bongo2', 4, 1.5), 'banga': (f'{EP}/voice/banga2', 0, 1.4)}
    S = [
        dict(clip='S1a', cut=(3.00, 9.40), dubs=[('bongo', 1, 6.50, 9.40)]),
        dict(clip='S2a', cut=(1.80, 9.60), dubs=[('banga', 1, 5.60, 8.40), ('bongo', 2, 7.90, 9.60)]),
        dict(clip='S3a', cut=(0.40, 7.60), dubs=[('banga', 2, 0.00, 3.50), ('bongo', 3, 5.00, 7.60)]),
        dict(clip='S4b', cut=(1.20, 9.80), dubs=[('banga', 3, 7.50, 9.80)]),
        dict(clip='S5b', cut=(0.90, 10.0), dubs=[('bongo', 4, 0.00, 3.00), ('bongo', 5, 6.60, 10.0)]),
    ]
    build(EP, 'output/ep007', 'bongo_ep007_v2', V, S)

def ep008():
    EP = 'episodes/ep008_dark_magico'
    V = {'bongo': (f'{EP}/voice/bongo2', 4, 1.5), 'banga': (f'{EP}/voice/banga2', 2, 1.5)}
    S = [
        dict(clip='S1b', cut=(0.80, 6.00), dubs=[('bongo', 1, 0.80, 4.80)]),
        dict(clip='S2a', cut=(1.20, 8.15), dubs=[('bongo', 2, 5.60, 8.15)], mute=[(1.80, 3.00)]),
        dict(clip='S3b', cut=(1.60, 8.00), dubs=[('banga', 1, 3.00, 5.20), ('bongo', 3, 5.20, 7.40)]),
        dict(clip='S4a', cut=(1.40, 9.20), dubs=[('banga', 2, 0.00, 4.00)]),
        dict(clip='S5b', cut=(1.50, 9.00), dubs=[('bongo', 4, 4.40, 7.60)]),
        dict(clip='S6b', cut=(0.00, 9.00), dubs=[('bongo', 5, 4.80, 7.00, 'muffle'), ('banga', 3, 6.80, 8.80)]),
    ]
    build(EP, 'output/ep008', 'bongo_ep008_v2', V, S)

def ep009():
    # "Bongo banana." ist gestrichen: Bongo spricht die Zeile im Clip nicht, dort bleibt sein Originalton.
    EP = 'episodes/ep009_bongo_brainrot'
    V = {'bongo': (f'{EP}/voice/bongo2', 4, 1.5), 'banga': (f'{EP}/voice/banga2', 2, 1.5)}
    S = [
        dict(clip='S1b', cut=(0.50, 6.50), dubs=[('bongo', 1, 1.80, 5.40)]),
        dict(clip='S2a', cut=(0.00, 8.50), dubs=[('banga', 1, 0.00, 4.00)]),
        dict(clip='S3a', cut=(2.60, 9.90), dubs=[('banga', 2, 7.20, 10.0)]),
        dict(clip='S4a', cut=(0.30, 9.60), dubs=[('bongo', 2, 5.80, 10.0)]),
        dict(clip='S5b', cut=(0.00, 9.60), dubs=[('banga', 3, 0.00, 3.50)]),
        dict(clip='S6a', cut=(0.30, 10.0), dubs=[('banga', 4, 6.40, 8.20), ('banga', 5, 7.90, 10.0)]),
    ]
    build(EP, 'output/ep009', 'bongo_ep009_v3', V, S)

def ep010():
    EP = 'episodes/ep010_bongo_papa'
    V = {'bongo': (f'{EP}/voice/bongo', 4, 1.5), 'banga': (f'{EP}/voice/banga', 2, 1.5)}
    S = [
        dict(clip='S1a', cut=(0.00, 5.20), dubs=[('banga', 1, 0.00, 2.20)]),                               # Banga pregnant.
        dict(clip='S2a', cut=(1.40, 6.40), dubs=[('bongo', 1, 2.40, 6.20)]),                               # Bongo papa!
        dict(clip='S3b', cut=(1.00, 7.80), dubs=[('banga', 2, 4.60, 8.00)]),                               # Banga... oops.
        dict(clip='S4b', cut=(0.00, 6.00), dubs=[('bongo', 2, 0.00, 4.50)]),                               # Bongo... suspicious.
        dict(clip='S5b', cut=(0.00, 6.20), dubs=[('bongo', 3, 0.00, 2.40), ('banga', 3, 2.60, 6.00)]),     # Bongo betrayed. / Banga sorry not sorry.
        dict(clip='S6b', cut=(1.20, 7.60), dubs=[('bongo', 4, 2.20, 5.20)]),                               # Bongo upgrade.
    ]
    build(EP, 'output/ep010', 'bongo_ep010_v1', V, S)

def ep010b():
    # Fassung 2: das Baby ist ein roter Eimer von einem anderen "Mann"; Bongo zaubert sich eine Koenigin aus seinem Eimer.
    EP = 'episodes/ep010_bongo_papa'
    V = {'bongo': (f'{EP}/voice/bongo', 4, 1.5), 'banga': (f'{EP}/voice/banga', 2, 1.5)}
    S = [
        dict(clip='S1a', cut=(0.00, 5.20), dubs=[('banga', 1, 0.00, 2.20)]),                               # Banga pregnant.
        dict(clip='S2a', cut=(1.40, 6.40), dubs=[('bongo', 1, 2.40, 6.20)]),                               # Bongo papa!
        dict(clip='N3b', cut=(0.60, 7.40), dubs=[('banga', 2, 5.20, 8.00)]),                               # Banga... oops.
        dict(clip='N4b', cut=(0.40, 7.60), dubs=[('banga', 3, 1.00, 4.40), ('bongo', 3, 4.20, 8.00)]),     # Banga sorry not sorry. / Bongo betrayed!
        dict(clip='N6a', cut=(0.00, 8.00), dubs=[('bongo', 5, 0.00, 3.50), ('bongo', 4, 4.80, 8.00)]),     # Bongo magico! / Bongo upgrade.
    ]
    build(EP, 'output/ep010', 'bongo_ep010_v2', V, S)

ALL = dict(ep006=ep006, ep007=ep007, ep008=ep008, ep009=ep009, ep010=ep010, ep010b=ep010b)
for n in (sys.argv[1:] or ALL):
    print(n); ALL[n]()

# Bongo Bucket – Flow-Pipeline (Stand 01.10.2026)

So entstehen die Folgen ab ep005. Kosten: nur Credits aus dem Google-Abo (Flow), sonst nichts.

## Ablauf
1. **Story** in 5–6 Einstellungen, jede mit einer klaren Aktion. Bongo sagt nur „Bongo" + kurzer Spruch, Banga nur „Banga" + kurzer Spruch.
2. **Schlüsselbilder** in Flow mit Nano Banana 2 (0 Credits, 9:16). Jedes Bild ist eine Bearbeitung des vorigen („Edit this exact image …"), damit Raum und Requisiten gleich bleiben. Jedes Bild vor der Verwendung ansehen.
3. **Clips** in Flow im Modus „Frames": Startbild + Endbild, Modell Omni 1.1 Flash, 720p, 8–10 s, 2 Varianten (24–30 Credits). Endbild einer Einstellung = Startbild der nächsten.
4. **Stimmen**: pro Figur EINE Aufnahme mit allen Zeilen (Modus „Bildelemente" + gespeicherte Stimme). `tools/voice_lines.py` schneidet sie in Zeilen.
5. **Sichtung**: `tools/review_clips.py <ordner>` erzeugt Standbild-Streifen, Sprach-Karte und erkannten Text je Clip.
6. **Schnitt**: `episodes/<folge>/edit.py` – beste Variante, Sprechstellen stumm, Stimmzeile darüber, Lautheit angleichen, 1080×1920.

## Figuren
- **Bongo**: `assets/characters/bongo_kitchen_base.jpg`, Stimme in Flow „Bongo English Spanish Higher", im Schnitt +4 Halbtöne.
- **Banga Manga**: `assets/characters/banga_manga_emo.jpg` (Emo-Anime-Äffin, Mango auf dem Kopf, goldene Bratpfanne). Stimme bisher Flow „Callirrhoe" – soll noch geändert werden.
- **Eimer**: gelber Smiley-Eimer, steht immer im Mittelpunkt.

## Folgen
| Folge | Datei | Inhalt |
|---|---|---|
| ep005 | `output/ep005/bongo_ep005_v2.mp4` | Bongo füttert den Eimer (Story zu brav) |
| ep006 | `output/ep006/bongo_ep006_v1.mp4` | Eimer geht fremd (Katze) |
| ep007 | `output/ep007/bongo_ep007_v1.mp4` | Banga or bucketo – erste Folge mit Banga Manga |

## Stolperfallen
- Endbild mit zwei weit offenen Augen → das Videomodell macht daraus eine Brille. Augen asymmetrisch lassen.
- Gleichnamige Bilder in der Flow-Auswahl per Bildvergleich bestimmen, nicht nach Reihenfolge.
- Manche Varianten bekommen eingebrannte Untertitel oder Sprechblasen → die andere Variante nehmen.
- `gen/inbox` enthält alle aus Flow geladenen Bilder und Clips, `episodes/*/tmp*` sind Zwischendateien (nicht im Repo).

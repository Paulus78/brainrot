# claude brainrot

Alles, was für die neueste gelungene Folge gebraucht wurde – als eigenständiges Paket.
Kosten: nur Credits aus dem Google-Abo (Flow). Bilder kosten 0 Credits, ein Clip mit 2 Varianten 24–30.

## Inhalt
| Ordner | Was drin ist |
|---|---|
| `characters/` | Referenzbilder: Bongo, Banga Manga, Eimer |
| `ep007_banga_or_bucket/keyframes/` | die 6 Schlüsselbilder der Folge (Start-/Endbilder der Clips) |
| `ep007_banga_or_bucket/clips/` | alle 10 Flow-Clips (je 2 Varianten pro Einstellung, mit Originalton) |
| `ep007_banga_or_bucket/voice/` | Stimmaufnahmen (`bongo2.mp4`, `banga2.mp4`) und die geschnittenen Zeilen (`line_N.wav`) |
| `ep007_banga_or_bucket/edit.py` | Schnittskript |
| `ep007_banga_or_bucket/bongo_ep007_v1.mp4` | fertiges Video |
| `tools/` | Sichtung, Zeilenschnitt, Hilfsserver für den Download aus Flow |

## Ablauf in 6 Schritten
1. **Story** in 5–6 Einstellungen, je eine klare Aktion. Bongo: „Bongo" + kurzer Spruch. Banga: „Banga" + kurzer Spruch.
2. **Schlüsselbilder** in Flow mit Nano Banana 2 (9:16). Jedes Bild ist eine Bearbeitung des vorigen, damit Raum und Requisiten gleich bleiben. Jedes Bild ansehen, bevor es verwendet wird.
3. **Clips** in Flow, Modus „Frames": Startbild + Endbild, Modell Omni 1.1 Flash, 720p, 8–10 s, 2 Varianten.
4. **Stimmen**: pro Figur eine Aufnahme mit allen Zeilen (Modus „Bildelemente" + gespeicherte Stimme), dann
   `python claude_brainrot/tools/voice_lines.py <aufnahme.mp4> <zielordner>`
5. **Sichtung**: `python claude_brainrot/tools/review_clips.py <clip-ordner>` → Standbild-Streifen, Sprach-Karte, erkannter Text.
6. **Schnitt**: `python claude_brainrot/ep007_banga_or_bucket/edit.py` (im Repo-Ordner ausführen; braucht ffmpeg und Python mit Pillow).

## Prompt-Bausteine
- **Bild bearbeiten:** `Edit this exact image. Keep the kitchen, the camera angle, the framing, the lighting and everything that is not mentioned identical. Vertical 9:16. …`
- **Clip-Vorspann:** `Static locked-off camera, one continuous shot, no cuts, no zoom, no camera movement. 3D cartoon animation, clear readable action. The brown creature never wears glasses: he has one big round eye and one smaller eye inside a single blue ring, a banana peel on his head.`
- **Clip-Schluss:** `No music. Absolutely no subtitles, no captions, no speech bubbles, no on-screen text. The yellow bucket keeps its printed smiley face and never moves by itself.`
- **Stimmaufnahme:** `Voice recording. … says exactly five short lines, each line only once, with a clear pause of one second of silence between the lines: "…" (Stimmung) … Audio: only his voice, completely dry.`

## Stimmen
- **Bongo:** Flow-Stimme „Bongo English Spanish Higher", im Schnitt 4 Halbtöne heller.
- **Banga:** bisher Flow-Stimme „Callirrhoe" – wird durch eine hellere, süßere Stimme ersetzt.

## Stolperfallen
- Endbild mit zwei weit offenen Augen → das Videomodell macht daraus eine Brille. Augen asymmetrisch lassen.
- Gleichnamige Bilder in der Flow-Auswahl per Bildvergleich bestimmen, nicht nach Reihenfolge.
- Varianten mit eingebrannten Untertiteln oder Sprechblasen aussortieren.
- Mit Start- und Endbild animiert das Modell von A nach B; ohne Endbild erfindet es frei.

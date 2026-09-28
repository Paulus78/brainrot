# Bongo Bucket Brainrot

Produktionsprojekt für den vertikalen 3D-Cartoon-Piloten **„Bongo fixes a fan“** mit der Figur Bongo.

## Aktueller Stand

- Episode 001 bleibt als dokumentierter Lernstand erhalten; ihr schwacher Hook, das künstliche Eimerschütteln, die hektische Verdichtung und der Stimmenwechsel wurden für Episode 002 ausdrücklich nicht übernommen.
- Episode 002 „Bongo Popcorno“ liegt als vollständiger 15-Sekunden-Finalkandidat unter `output/pilot_002/pilot_002_final_v1.mp4` vor.
- Der neue Hook beginnt direkt mit dem Zahn-PING, der Eimer bleibt beim Ritual am Boden, drei Klopfer ersetzen das misslungene Schütteln und der Payoff erhält einen langen lesbaren Hold.
- `Bucketo.` und `Bongo snacko.` stammen aus einer einzigen Flow-Aufnahme. Der zweite Stimmversuch wurde wegen eines erneuten Hochtonsprungs verworfen; der akzeptierte Mix bleibt zwischen den Zeilen innerhalb von 0,67 Halbtönen.
- Alle akzeptierten und verworfenen Rohversuche, Prompts, Messungen und reproduzierbaren Schnittskripte bleiben als Produktionshistorie erhalten.

Ausführliche Fortschritts- und Qualitätsinformationen stehen in:

- `episodes/pilot_001/production_status.md`
- `episodes/pilot_001/qc/keyframe_qc.md`
- `episodes/pilot_001/qc/video_qc.md`
- `episodes/pilot_001/revision_v2/status.md`
- `episodes/pilot_001/revision_v2/video_qc.md`
- `episodes/pilot_002/status.md`
- `episodes/pilot_002/storyboard_qc.md`
- `episodes/pilot_002/picture_cut_qc.md`
- `episodes/pilot_002/audio/voice_qc.md`
- `output/pilot_002/final_qc.md`
- `docs/production_learnings_and_next_story.md`
- `episodes/pilot_001/episode.json`

## Projektstruktur

- `sources/` – unveränderte kreative Vorgaben und Startdokumente
- `assets/character_master/` – verbindliche Bongo-Referenz
- `episodes/pilot_001/keyframes/` – freigegebene Szenenbilder
- `episodes/pilot_001/video_raw/` – bisherige Roh-Render
- `episodes/pilot_001/voice/` – Stimmprototypen
- `episodes/pilot_001/prompts/` – reproduzierbare Bild- und Stimm-Prompts
- `episodes/pilot_001/qc/` – Qualitätsprüfungen und Entscheidungen
- `episodes/pilot_001/revision_v2/` – überarbeitete Ursache-Wirkung-Fassung und V2-QC
- `episodes/pilot_002/` – Popcorno-Planung, Continuity, Storyboard, Audio und QC
- `output/pilot_001/` – frühere Pilotfassungen
- `output/pilot_002/` – Bildschnitt, Voice-only-Prüfung und finaler Kandidat
- `src/edit/` – reproduzierbare Animatic-, Hybrid-, Analyse- und Finalschnitt-Skripte

## Auf einem anderen Rechner weiterarbeiten

```bash
git clone https://github.com/Paulus78/brainrot.git
cd brainrot
```

Der aktuelle Flow-Arbeitsbereich ist in `episodes/pilot_001/episode.json` verlinkt. Die heruntergeladenen Medien und alle verwendeten Prompts sind zusätzlich im Repository gesichert, damit der Stand nicht ausschließlich von der lokalen Flow-Sitzung abhängt.

Für das Animatic wird Python mit Pillow benötigt:

```bash
python3 -m pip install Pillow
python3 src/edit/compose_animatic.py
```

Für den finalen Videoschnitt wird zusätzlich `ffmpeg` benötigt:

```bash
python3 src/edit/compose_v2_final.py
```

Falls `ffmpeg` nicht im Suchpfad liegt, kann sein vollständiger Pfad über die Umgebungsvariable `FFMPEG` gesetzt werden.

## Arbeitsregel

Nach jedem belastbaren Produktionsschritt:

1. Ergebnis visuell bzw. akustisch prüfen.
2. QC-Entscheidung und Status aktualisieren.
3. Nur reproduzierbare, nachvollziehbare Dateien committen.
4. Den neuen Stand auf `main` pushen.

Keine echten API-Schlüssel oder Zugangsdaten in das Repository legen. Dafür ausschließlich lokale Umgebungsvariablen oder eine nicht versionierte `config.yaml` verwenden.

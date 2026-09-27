# Bongo Bucket Brainrot

Produktionsprojekt für den vertikalen 3D-Cartoon-Piloten **„Bongo fixes a fan“** mit der Figur Bongo.

## Aktueller Stand

- Die überarbeitete V2-Fassung mit expliziter Ursache-Wirkung-Kette liegt unter `output/pilot_001/revision_v2/pilot_001_v2_final.mp4` vor.
- Die kreative Nachprüfung bewertet V2 trotz besserer Kontinuität noch als zu statisch, zu schnell geschnitten und stimmlich nicht konsistent genug für eine Veröffentlichung.
- Auch das handgehaltene Eimerschütteln und der zu schwache Ventilator-Hook gelten als nicht bestanden und werden nicht unverändert wiederverwendet.
- Learnings, neue verbindliche Produktionsregeln und der empfohlene Plan für Episode 002 „Bongo Popcorno“ stehen in `docs/production_learnings_and_next_story.md`.
- Beide Fassungen und alle akzeptierten sowie verworfenen Rohversuche bleiben als Produktionshistorie erhalten.
- Für Episode 002 sind Masterprompt, Continuity-Tabelle und vier geprüfte Storyboard-Keyframes fertig. Der 15-Sekunden-Stummfilm-Animatic liegt unter `output/pilot_002/`.
- Der Zustands- und Unterhaltungstest des Storyboards ist bestanden. Als nächstes wird ausschließlich der Zahn-PING-Hook in Veo als Bewegung prototypisiert; spätere Motion-Shots bleiben bis zu dessen Freigabe gesperrt.

Ausführliche Fortschritts- und Qualitätsinformationen stehen in:

- `episodes/pilot_001/production_status.md`
- `episodes/pilot_001/qc/keyframe_qc.md`
- `episodes/pilot_001/qc/video_qc.md`
- `episodes/pilot_001/revision_v2/status.md`
- `episodes/pilot_001/revision_v2/video_qc.md`
- `episodes/pilot_002/status.md`
- `episodes/pilot_002/storyboard_qc.md`
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
- `episodes/pilot_002/` – Popcorno-Planung, Continuity, Storyboard und QC
- `output/pilot_001/` – aktuelle Vorschauen/Animatics
- `src/edit/` – lokales Animatic-Skript

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

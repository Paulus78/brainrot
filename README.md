# Bongo Bucket Brainrot

Produktionsprojekt für den vertikalen 3D-Cartoon-Piloten **„Bongo fixes a fan“** mit der Figur Bongo.

## Aktueller Stand

- Vier vertikale 9:16-Keyframes sind erstellt und qualitätsgeprüft.
- Der 12-Sekunden-Animatic enthält alle vier finalen Keyframes.
- Für Shot 04 liegen drei Video-Versuche vor; Veo-Versuch 02 ist die stabilste stumme Bewegungsbasis.
- Eine natürlichere, benutzerdefinierte Bongo-Stimme wurde in Google Flow erstellt und in Shot-04-Versuch 03 verwendet.
- Die lokalen macOS-Stimmen A/B/C sind nur verworfene Timing-Prototypen und dürfen nicht im finalen Mix verwendet werden.
- Shot 02 ist mit der neuen Stimme animiert und nach visueller/action-basierter QC akzeptiert.

Ausführliche Fortschritts- und Qualitätsinformationen stehen in:

- `episodes/pilot_001/production_status.md`
- `episodes/pilot_001/qc/keyframe_qc.md`
- `episodes/pilot_001/qc/video_qc.md`
- `episodes/pilot_001/episode.json`

## Projektstruktur

- `sources/` – unveränderte kreative Vorgaben und Startdokumente
- `assets/character_master/` – verbindliche Bongo-Referenz
- `episodes/pilot_001/keyframes/` – freigegebene Szenenbilder
- `episodes/pilot_001/video_raw/` – bisherige Roh-Render
- `episodes/pilot_001/voice/` – Stimmprototypen
- `episodes/pilot_001/prompts/` – reproduzierbare Bild- und Stimm-Prompts
- `episodes/pilot_001/qc/` – Qualitätsprüfungen und Entscheidungen
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

## Arbeitsregel

Nach jedem belastbaren Produktionsschritt:

1. Ergebnis visuell bzw. akustisch prüfen.
2. QC-Entscheidung und Status aktualisieren.
3. Nur reproduzierbare, nachvollziehbare Dateien committen.
4. Den neuen Stand auf `main` pushen.

Keine echten API-Schlüssel oder Zugangsdaten in das Repository legen. Dafür ausschließlich lokale Umgebungsvariablen oder eine nicht versionierte `config.yaml` verwenden.

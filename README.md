# Bongo Bucket Brainrot

Produktionsprojekt für den vertikalen 3D-Cartoon-Piloten **„Bongo fixes a fan“** mit der Figur Bongo.

## Aktueller Stand

- Vier vertikale 9:16-Keyframes sind erstellt und qualitätsgeprüft.
- Der 12-Sekunden-Animatic enthält alle vier finalen Keyframes.
- Shot 04 Versuch 04 ist mit stabiler Bananenpropeller-Bewegung und beiden vorgesehenen Voice-Zeilen akzeptiert.
- Eine natürlichere, benutzerdefinierte Bongo-Stimme wurde in Google Flow erstellt und in allen vier akzeptierten Shots verwendet.
- Die lokalen macOS-Stimmen A/B/C sind nur verworfene Timing-Prototypen und dürfen nicht im finalen Mix verwendet werden.
- Shot 02 ist mit der neuen Stimme animiert und nach visueller/action-basierter QC akzeptiert.
- Shot 01 ist mit der neuen Stimme animiert und nach visueller/identitätsbasierter QC akzeptiert.
- Shot 03 Versuch 01 bleibt als Fallback erhalten; Versuch 02 ist mit drei klar getrennten, zunehmend stärkeren Schüttelbewegungen akzeptiert.
- Der vollständige 12-Sekunden-Pilot liegt als `output/pilot_001/pilot_001_final.mp4` vor.
- Der finale Schnitt ist reproduzierbar über `src/edit/compose_final.py`; technische und visuelle QC sind dokumentiert.

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

Für den finalen Videoschnitt wird zusätzlich `ffmpeg` benötigt:

```bash
python3 src/edit/compose_final.py
```

Falls `ffmpeg` nicht im Suchpfad liegt, kann sein vollständiger Pfad über die Umgebungsvariable `FFMPEG` gesetzt werden.

## Arbeitsregel

Nach jedem belastbaren Produktionsschritt:

1. Ergebnis visuell bzw. akustisch prüfen.
2. QC-Entscheidung und Status aktualisieren.
3. Nur reproduzierbare, nachvollziehbare Dateien committen.
4. Den neuen Stand auf `main` pushen.

Keine echten API-Schlüssel oder Zugangsdaten in das Repository legen. Dafür ausschließlich lokale Umgebungsvariablen oder eine nicht versionierte `config.yaml` verwenden.

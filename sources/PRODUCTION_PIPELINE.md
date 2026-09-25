# Production Pipeline – Bongo Bucket

## 1. Architekturprinzip

Module:

```text
src/
  config/
  ideation/
  episode/
  image/
  video/
  voice/
  audio/
  edit/
  qc/
  manifests/
```

Kreative Logik nicht in Provider-Code verstecken.

## 2. Pipeline

```text
Concept
→ Episode manifest
→ Shot decomposition
→ Keyframe prompts
→ Keyframe generation
→ Character QC
→ Video generation per shot
→ Voice/TTS
→ Jingle + SFX
→ Edit
→ Technical QC
→ Creative QC
→ Final export + postmortem
```

## 3. Provider-Strategie

### Bild
Default: kosteneffizientes Modell mit 9:16 und guter Character-Konsistenz.

Stand der Spec:
- Gemini 3.1 Flash Lite Image ist eine sinnvolle günstige Option.
- Alternativen dürfen nach dokumentiertem Vergleich gewählt werden.

### Video
Default:
- Veo 3.1 Lite
- Image-to-Video bevorzugen
- separate `referenceImages` bei Lite nicht voraussetzen
- Keyframe nahe am gewünschten ersten Videoframe bauen

### Voice
- Gemini 3.8 Flash TTS für Voice-Design/Audition
- Flash-Lite für Serienproduktion testen
- persistente Voice bevorzugen

Vor echtem API-Code aktuelle Doku prüfen.

## 4. Repo-Struktur

```text
assets/
  character_master/
  bucket_master/
  sfx/
  music/
episodes/
  pilot_001/
    episode.json
    prompts/
    keyframes/
    video_raw/
    voice/
    audio/
    edit/
    qc/
output/
  pilot_001/
    pilot_001_master.mp4
    pilot_001_clean.mp4
    thumbnail.png
    manifest.json
    postmortem.md
```

## 5. Dry-Run

Ohne kostenpflichtige Calls:
- Episode JSON
- Shotliste
- Bildprompts
- Video-Prompts
- Voice-Skript
- Audio-Cue-Sheet
- Anzahl Calls
- Kostenschätzung nur aus aktuell verifizierten Preisen

## 6. Keyframes

Für jeden Shot:
1. Bongo-Master referenzieren, wenn möglich.
2. nur nötige Props.
3. Kamera festlegen.
4. Pose nahe am Start.
5. Hintergrund simpel.
6. QC.

Ablehnen bei:
- falschem Gesicht
- fehlender Banane
- falschem Eimer
- zusätzlichen Figuren
- deformiertem Hauptprop
- schlechter Lesbarkeit

## 7. Video

Prompt beschreibt primär **Bewegung**.

Gut:
> Bongo stays in place and looks from the motionless fan to the yellow bucket. He tilts his head once. His ears make a small soft bounce. The fan remains still. Static eye-level camera. Subtle motion only.

Transformationen möglichst per Cut lösen.

## 8. Retry

Pro Shot:
- Attempt 1
- gezielte Korrektur
- Attempt 2
- Shot vereinfachen
- Attempt 3
- Blocker dokumentieren

## 9. Voice

1. A/B/C Audition
2. Voice wählen
3. Phrasen ggf. separat rendern
4. WAV speichern
5. Mix

## 10. Editing

- FFmpeg oder äquivalent
- harte Cuts okay
- 9:16
- tote Frames trimmen
- Comedy-Pausen bewusst
- Voice exakt auf Action
- „Bongo fixo“ nicht überdecken

## 11. QC

Technisch:
- Datei vorhanden
- Länge plausibel
- 9:16
- Audio vorhanden
- keine kaputten Frames

Kreativ:
- Character konsistent
- Payoff verständlich
- Brainrot-Faktor hoch genug
- nicht zu random

## 12. Manifest

Speichern:
- Modell-ID
- SDK-Version
- Prompt
- Input-Hashes
- Outputpfad
- Dauer
- Parameter
- Versuch
- Auswahlgrund
- QC

## 13. Kostenkontrolle

Optimieren in dieser Reihenfolge:
1. Fehlversuche reduzieren
2. Shots vereinfachen
3. günstigere Modelle
4. Volumen erhöhen

## 14. Serienmodus

Erst nach Pilot:

```text
idea generator
→ idea scoring
→ shortlist
→ manifests
→ keyframes
→ QC
→ video
→ audio
→ edit
→ QC
→ ready_to_post
```

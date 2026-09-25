# Startprompt für Codex

Lies zuerst `AGENTS.md`, dann alle dort referenzierten Dateien unter `docs/`, danach `config.example.yaml` und `schemas/episode.schema.json`.

## Aufgabe

Baue die **kleinste robuste Produktionspipeline**, mit der ein sehr guter erster **Bongo-Bucket-Pilot-Short** erzeugt werden kann.

Dein Ziel ist nicht maximale Automatisierung, sondern ein Pilot, der:
- visuell sofort verständlich,
- absurd und meme-tauglich,
- technisch sauber,
- charakterkonsistent,
- akustisch wiedererkennbar
ist.

## Konkret

Produziere `pilot_001` aus `docs/PILOT_EPISODE.md`.

Arbeite in dieser Reihenfolge:

1. Repository und Laufzeit prüfen.
2. Verfügbare Credentials erkennen, ohne Secrets auszugeben.
3. Aktuelle offizielle Dokumentation der tatsächlich eingesetzten Bild-, Video- und TTS-Modelle prüfen.
4. Provider-Adapter minimal implementieren.
5. `episode.json` nach `schemas/episode.schema.json` erzeugen.
6. Dry-Run:
   - finale Shotliste,
   - Keyframe-Prompts,
   - Video-Prompts,
   - Voice-Skripte,
   - SFX-/Musikplan,
   - erwartete Kosten soweit aus API-Preisen ableitbar.
7. Drei Voice-Auditions A/B/C mit demselben Audition-Skript erzeugen.
8. Einen Voice-Kandidaten für den Pilot auswählen und die Begründung in `output/pilot_001/voice_choice.md` dokumentieren. Falls keine objektive Auswahl möglich ist, exportiere drei Pilot-Audio-Previews statt zu raten.
9. Keyframes für jeden Shot erzeugen.
10. Jeden Keyframe gegen die Character Bible prüfen.
11. Nur akzeptierte Keyframes animieren.
12. Shots einzeln generieren.
13. Voice, Jingle, SFX und Ambiente mischen.
14. Pilot schneiden.
15. `docs/QUALITY_GATES.md` anwenden.
16. Nur fehlerhafte Elemente erneut erzeugen.
17. Finale Datei exportieren.
18. `output/pilot_001/postmortem.md` schreiben.

## Wichtige kreative Einschränkungen

- Keine Nebenfigur.
- Keine zusätzlichen Dialoge.
- Kein komplexes Lip-Sync.
- Keine komplizierte Kamerafahrt.
- Kein Wechsel der Location.
- Pro Veo-Shot eine Hauptaktion.
- Humor nicht durch zusätzliche Objekte aufblasen.
- Der gelbe Eimer bleibt identisch.
- Bongo bleibt weird-cute.
- Der Payoff ist eine **Banane als rotierender Ventilatorflügel/Propeller**.
- Das finale „Bongo fixo“ muss trocken und stolz wirken.

## Entscheidungsregel

Wenn du zwischen „größer/komplexer“ und „einfacher/klarer“ wählen musst:

> **Wähle einfacher/klarer.**

Wenn du zwischen „technisch perfekt, aber langweilig“ und „leicht absurd, aber robust machbar“ wählen musst:

> **Wähle absurd + robust machbar.**

Stoppe nach Pilot + QC + Postmortem.

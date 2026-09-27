# Pilot revision V2 — status

Updated: 2026-09-27 (Europe/Berlin)

## Current state

- All five continuity keyframes: PASS.
- 12-second V2 animatic: READY.
- Individual shot animation and voice generation: COMPLETE.
- Shot 1 animation: PASS after one corrective retry. The accepted take preserves the blue eye ring, single left sandal, damaged motionless fan and button-press reaction.
- Shot 2 animation: PASS after one corrective retry. The complete fan visibly crosses the rim and disappears; the separate banana is then released and fully vanishes below the rim.
- Shot 3 animation: PASS. Three separated motion/voice beats read small, medium and strong; Bongo returns to center and nothing leaves the bucket.
- Shot 4 animation: PASS. The same fan visibly completes its slide across the bucket rim, lands upright and holds with the banana propeller completely still.
- Shot 5 animation: PASS. The banana propeller spins, the base remains planted, Bongo holds the proud pose and the payoff line is visibly delivered.
- Final 12-second edit: PASS — `output/pilot_001/revision_v2/pilot_001_v2_final.mp4`.
- Full-sequence visual and technical QC: PASS. Runtime is 12.022 seconds at 360 × 640, 24 fps; audio is 48 kHz stereo at -15.7 LUFS integrated with -1.0 dBFS true peak.
- V2 revision: COMPLETE and ready for use on another computer after cloning the GitHub repository.

## Required quality gates

- Shot 1: the fan reads as broken in a still frame without dialogue.
- Shot 2: the complete same fan visibly crosses the bucket rim and disappears inside; one banana follows.
- Shot 3: fan and banana stay hidden; exactly three separated shakes read small / medium / strong.
- Shot 4: the same fan visibly exits the bucket already fitted with a banana propeller before spinning.
- Shot 5: the banana propeller spins; fan body stays planted; Bongo's wind reaction and dry final line remain clear.
- No unexplained object swaps, duplicate props, teleportation or continuity jumps.

## Keyframe review

- Shot 1: PASS — compact grey fan is visibly damaged, drooped and motionless.
- Shot 2: PASS — the same damaged fan is held directly above the open bucket; the intact banana remains visible beside it.
- Shot 3: PASS — Bongo grips the closed visual setup with both hands; fan and banana are fully hidden.
- Shot 4: PASS — the repaired fan visibly crosses the bucket rim while emerging; the banana propeller is attached and still.
- Shot 5: PASS — the same repaired fan stands upright beside the empty bucket; the banana propeller is ready to start.

The five stills use the same Bongo design, warm workshop, yellow smiley bucket and compact grey fan. Minor pose and angle changes remain within shot-to-shot continuity tolerance. The complete cause-and-effect chain reads without dialogue in the animatic.

## Final-sequence review

- PASS — broken fan is established before Bongo handles it.
- PASS — the complete fan visibly enters the bucket, followed by one banana.
- PASS — the loaded bucket receives exactly three separated shakes.
- PASS — the repaired fan visibly exits with its banana propeller attached and still.
- PASS — the propeller then spins while the fan body stays planted and Bongo holds the proud payoff pose.
- PASS — representative frames retain Bongo's blue eye ring and single left sandal.
- PASS — hard cuts preserve the intended simple, readable structure without adding objects or characters.

The reproducible assembly script is `src/edit/compose_v2_final.py`. It uses only the five accepted V2 takes and fixes their total edited duration at 12.0 seconds while preserving audio pitch.

## Previous cut

The first final candidate remains preserved in `output/pilot_001/pilot_001_final.mp4` as a superseded continuity reference. It is not the target for the revised story.

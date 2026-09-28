# Pilot 002 — picture cut quality review

Updated: 2026-09-28 (Europe/Berlin)

## Accepted review file

Picture cut: `output/pilot_002/pilot_002_picture_cut_v1.mp4`

Muted review copy: `output/pilot_002/pilot_002_picture_cut_v1_silent.mp4`

## Edit timing

| Unit | Source | Used duration | Edit range | Policy |
| --- | --- | ---: | ---: | --- |
| Tooth-PING hook | `hook_01_hybrid_v1.mp4` | 2.50 s | 0.00–2.50 s | Action unchanged; final hold shortened by 0.50 s |
| Banana drop | `banana_02_hybrid_v1.mp4` | 3.20 s | 2.50–5.70 s | Action unchanged; empty-bucket hold shortened by about 0.82 s |
| Three taps and self-rumble | `taps_03_hybrid_v3.mp4` | 4.25 s | 5.70–9.95 s | Entire accepted unit retained |
| Popcorn payoff | `payoff_04_hybrid_v2.mp4` | 5.00 s | 9.95–14.95 s | Entire accepted unit retained |

Measured file duration is 14.959 seconds because of AAC frame padding.

## Technical QC

- Format: PASS — H.264/AAC MP4.
- Frame: PASS — vertical 720 × 1280 at 24 fps.
- Runtime: PASS — 14.959 seconds, matching the approximately 15-second target.
- Black frames: PASS — no black interval of 0.08 seconds or longer detected.
- Speed policy: PASS — no accepted action clip is accelerated. Only existing final holds are trimmed.
- Rebuild path: PASS — `src/edit/build_picture_cut.sh` reproduces the same timing from the four accepted units.

## First-view silent story test

- Immediate hook: PASS — the first frame begins with the kernel at Bongo's tooth and the bucket visible.
- Ingredient one: PASS — the single kernel reaches the bucket and is absent afterward.
- Ingredient two: PASS — one intact banana visibly enters the same bucket and disappears.
- Ritual count: PASS — three paw-to-rim contacts remain individually readable.
- Anticipation: PASS — the motionless pause is preserved before the bucket self-rumbles.
- Weight: PASS — the ritual bucket never lifts, slides or enters Bongo's hands.
- Payoff source: PASS — the first popcorn pieces visibly emerge from the open bucket.
- Escalation: PASS — small burst, broad fountain and giant mound are clearly ordered.
- Final gag: PASS — Bongo, the bucket and one held snack remain readable in a stable hold longer than 3.5 seconds.
- Continuity: PASS — Bongo retains the head banana, tooth, blue eye ring and single left sandal in every accepted unit.

## Creative QC

- The four units read as one causal chain rather than five unrelated micro-clips.
- Hard cuts occur only at completed thoughts: kernel result to banana idea, banana result to ritual, self-rumble reaction to eruption.
- The longest uninterrupted time is reserved for the strongest image, not for setup.
- The payoff begins before ten seconds and occupies the final third of the video.
- The edit is ready for one continuous master voice session; dialogue must not be regenerated per shot.

## Remaining gate

Create one voice master containing both lines in the same warm, dry, mid-low register:

1. `Bucketo.` — place after the banana disappears, during the confident hold.
2. `Bongo snacko.` — place during the final satisfied hold.

Reject any high-pitched surprise voice, different resonance between lines, robotic cadence or line-by-line synthesis mismatch.

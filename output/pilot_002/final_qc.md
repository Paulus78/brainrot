# Pilot 002 — final candidate quality review

Updated: 2026-09-28 (Europe/Berlin)

Reviewed file: `output/pilot_002/pilot_002_final_v1.mp4`

Release status updated 2026-09-29: **REJECTED FOR MOTION FLUIDITY**. The earlier technical pass remains valid, but the file is now classified as a motion/story proof rather than a final episode.

## Technical result

- Duration: 14.959 seconds.
- Format: H.264 video with AAC mono audio.
- Frame: 720 × 1280, vertical 9:16, 24 fps.
- Black-frame test: PASS; no black interval of 0.08 seconds or longer.
- Integrated loudness: -20.5 LUFS.
- True peak: -1.1 dBFS.
- Picture integrity: PASS; the accepted Picture Cut V1 video stream is copied without another visual encode.
- Rebuild path: `src/edit/build_episode_002_final.sh`.

## Story and entertainment result

- Hook by 0.8 seconds: PASS — tooth impact and flying kernel are immediate.
- Ingredient chain: PASS — one kernel and then one whole banana enter the same bucket.
- Failed shake replaced: PASS — the bucket stays planted while three contacts, a pause and self-rumble create the ritual.
- Payoff scale: PASS — the eruption grows from the bucket into a large readable mound.
- Dialogue placement: PASS — both lines occur only after their corresponding visual action has completed.
- Final hold: PASS — `Bongo snacko.` ends more than two seconds before the video ends.

## Voice result

- Both final lines originate from one uninterrupted Flow take.
- The accepted source take differs by 0.95 semitones between lines; the placed final regions differ by 0.67 semitones.
- The second audition was rejected because its second line rose by 4.11 semitones and an unwanted sound appeared near the end.
- Full measurements and source decisions are recorded in `episodes/pilot_002/audio/voice_qc.md`.

## Final verdict

**TECHNICAL PASS / CREATIVE MOTION FAIL.** The story, timing, object continuity and accepted voice master remain useful, but the blend-based pose changes are not sufficiently fluid for publication. Rebuild the four motion units according to `episodes/pilot_002/motion_rebuild_v2.md`; do not try to hide the problem with more cross-dissolves or sound design.

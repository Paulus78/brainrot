# Pilot 002 — status

Updated: 2026-09-28 (Europe/Berlin)

## Current state

- Story direction selected for production planning: `Bongo Popcorno`.
- Master prompt: READY.
- Continuity table and rejection rules: READY.
- Four storyboard prompts: READY.
- Storyboard keyframes: PASS. Four accepted frames are stored under `episodes/pilot_002/keyframes/`.
- Frame 03 required one corrective retry because the first version did not read as a completed tap.
- Silent animatic: READY at `output/pilot_002/pilot_002_silent_animatic.webp` and `.gif`.
- Animatic technical check: PASS — four 1080 × 1920 frames with holds of 3.0 / 4.0 / 3.5 / 4.5 seconds, totaling exactly 15.0 seconds.
- Veo motion prompts and per-shot hard gates: READY in `motion_prompts.md` and `motion_qc.md`.
- Veo Prototype 01 Attempt 01: REJECTED after frame-level review. The kernel entered too slowly and the bare right foot gained a second blue sandal. The raw attempt is preserved under `video_raw/rejected/` for traceability.
- Veo Prototype 01 Attempts 01–04: all rejected and preserved for traceability. The repeated failure mode was unreliable small-object motion: slow entry, object morphing, reappearance or duplication.
- Prototype 01 Hybrid V1: PASS at `video_raw/accepted/hook_01_hybrid_v1.mp4`. It uses three locked states and deterministic timing instead of unreliable interpolation.
- Prototype 02 raw Veo Attempt 01: rejected because a banana stem fragment remained visible inside the bucket.
- Prototype 02 Hybrid V1: PASS at `video_raw/accepted/banana_02_hybrid_v1.mp4`; the verified release motion cuts to a clean empty-bucket hold before the stem error.
- Prototype 03 raw Veo Attempt 01: rejected because Bongo waved instead of tapping and the bucket floated/bounced off the floor.
- Prototype 03 Hybrid V1: rejected because hard state cuts made the taps feel mechanical.
- Prototype 03 Hybrid V2: structurally correct but rejected because Bongo did not react and the beat remained emotionally flat.
- Prototype 03 Hybrid V3: PASS at `video_raw/accepted/taps_03_hybrid_v3.mp4`. It contains three increasing contacts, a clear silent pause, a planted self-rumble and a delayed startled reaction.
- Prototype 04 Hybrid V1: rejected because the long dissolves created extended double contours around eyes and paws.
- Prototype 04 Hybrid V2: PASS at `video_raw/accepted/payoff_04_hybrid_v2.mp4`. The eruption begins inside the bucket, grows into a large mound, preserves Bongos readable face and holds the final gag for more than 3.5 seconds.
- All four visual motion prototypes: PASS.
- Picture Cut V1: PASS at `output/pilot_002/pilot_002_picture_cut_v1.mp4`; 14.959 seconds, 720 × 1280, 24 fps, no black interval and no action acceleration.
- Muted first-view story test: PASS; review copy stored at `output/pilot_002/pilot_002_picture_cut_v1_silent.mp4`.
- Final voice: PASS. Both lines were generated in one uninterrupted Google Flow Omni 1.1 Flash take in Chrome. Take 1 was accepted; Take 2 was rejected after it raised the second line by 4.11 semitones and added an unwanted trailing sound.
- Final Candidate V1: READY at `output/pilot_002/pilot_002_final_v1.mp4`; 14.959 seconds, 720 × 1280, 24 fps, -20.5 LUFS and -1.1 dBFS true peak.
- Voice-only review: READY at `output/pilot_002/pilot_002_voice_only_v1.wav`.

## Non-negotiable improvements over Pilot 001 V2

- A visual failure or gag occurs within the first 0.8 seconds.
- The bucket remains planted; no hand-held side-to-side shake.
- Three to four longer narrative units replace five rushed micro-clips.
- No final dialogue is generated separately inside each video shot.
- No story clip will be repaired through speed changes above approximately 1.15×.
- Creative approval requires a silent-story test, voice-identity test and entertainment test in addition to technical QC.

## Current quality verdict

- Tooth-PING hook: PASS at storyboard level.
- Same-character and same-bucket continuity: PASS within storyboard tolerance.
- Planted bucket replacing the failed hand-held shake: PASS in accepted motion.
- Large banana-popcorn payoff: PASS in accepted motion.
- Silent cause-and-effect chain from tooth impact through final mound: PASS in motion.
- Same-voice identity across both final lines: PASS by one-session source, +0.67-semitone final median difference and 0.07 dB final level difference.
- Dialogue placement on completed visual beats: PASS.
- Combined technical export: PASS.

## Next gate

Run one human listening pass on `output/pilot_002/pilot_002_final_v1.mp4`, concentrating only on perceived naturalness and comic character. The visual story, timing, voice identity and technical export are already locked. If a future voice take is preferred, replace only the single master in `episodes/pilot_002/audio/accepted/` and rebuild with `src/edit/build_episode_002_final.sh`.

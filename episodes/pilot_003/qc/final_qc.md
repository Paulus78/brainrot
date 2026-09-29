# Pilot 003 — final V1 quality review

Reviewed: 2026-09-29 (Europe/Berlin)

## Verdict

`output/pilot_003/pilot_003_bananacorno_v1.mp4` is **rejected after full-sequence user review**. The earlier working-master verdict was incorrect. Individual clips contain continuous motion, but both joins break scene, prop and camera continuity, while the three native Veo sound beds do not form one coherent soundtrack.

The detailed postmortem and replacement workflow are in `docs/postmortem_pilot_003_and_process_v4.md`.

## What now works

- The first frame is the actual story hook: Bongo is already wrestling with an absurdly oversized corn cob over the smiley bucket.
- All three scenes contain real continuous Veo animation rather than crossfades between still poses.
- The cob visibly disappears into the bucket before the ritual begins.
- The ritual is one large wind-up and slam with body weight, bucket squash and rebound; the failed artificial bucket shaking is gone.
- The payoff has a warning pop, a continuous popcorn fountain, burial, re-emergence and a visible bite.
- The three longer action units remain readable and do not feel like a rapid slideshow.
- Only the accepted, pitch-consistent `Bongo snacko.` line is used. No high `perfecto` voice remains.

## Disqualifying failures

- The garage dressing, camera distance and bucket geometry change visibly at both cuts.
- The accepted slam begins with a full bucket immediately after the previous clip ended with a different empty bucket.
- The hook's giant cob inherits a banana-like peel at the top. It remains instantly readable as absurd brainrot food and does not obscure the cause-and-effect chain.
- The independently generated sound beds change texture and meaning at the cuts; global normalization does not repair them.
- The second join begins with popcorn already visible, so the payoff starts before its cause has been clearly presented.

## Technical checks

- Duration: 19.96 s.
- Frame: 1080 × 1920, 9:16.
- Frame rate: 24 fps.
- Video: H.264, yuv420p.
- Audio: AAC stereo, 48 kHz.
- Integrated loudness: -15.5 LUFS.
- True peak: -0.8 dBTP.
- Black-frame detection: no black sections reported.

## Process decision

The independent reference-only scene process is not validated for multi-shot continuity. Future work must use one approved canonical world, one base clip and Flow scene extension. Native clip audio must be muted and rebuilt from separate ambience, Foley, hard effects and voice tracks after picture lock.

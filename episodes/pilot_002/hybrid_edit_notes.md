# Pilot 002 — hybrid edit strategy

Updated: 2026-09-27 (Europe/Berlin)

## Why the hook changed

Four Veo motion attempts proved that a tiny rigid object travelling through a long 9:16 shot is not reliable enough for the story gate. The model repeatedly slowed, duplicated, morphed or reintroduced the corn kernel even when start and end frames were locked.

The accepted production method therefore separates image generation from deterministic motion:

1. `frame_01_tooth_ping.png` establishes the tooth impact immediately.
2. `frame_01c_kernel_at_rim.png` shows the same single kernel immediately above the open rim.
3. `frame_01d_rim_empty.png` confirms that the kernel is fully hidden inside the bucket.
4. The three locked states are cut together at normal speed with one crisp PING and one quiet plink. No AI interpolation is allowed between the kernel states.

This is a deliberate clarity decision, not a fallback to frantic montage. The complete hook remains one causal unit and holds on Bongo looking into the bucket after the entry.

## Hook timing target

- 0.00–0.46 s: tooth-impact state, immediate PING and tiny punch-in.
- 0.46–0.71 s: kernel directly above the rim.
- 0.71–3.00 s: empty bucket confirmation and confused look-down hold.

## Acceptance gate

- The hook begins in action.
- Exactly one kernel is visible before the entry and none afterward.
- The bucket is visibly empty in the confirmation state; no popcorn appears.
- Bongo keeps one attached tooth, the blue right-eye ring, attached head peel and exactly one blue sandal on the raised left foot.
- The transition is readable muted and at normal playback speed.
- No source clip is accelerated.
- The hold after entry lasts more than 1.5 seconds.

## Rule for later beats

Use Veo only for motions it can preserve under frame-level QC. For critical object transfers and countable contacts, prefer locked state cuts or deterministic motion over additional retries that repeat a known failure mode.

## Banana-drop application

The first banana motion candidate contained a good release and rim crossing but left a stem fragment visible inside the bucket. The accepted `banana_02_hybrid_v1.mp4` keeps the verified first 18 frames at normal speed and cuts to the cleaned empty-bucket state `frame_02c_post_drop_clean.png`. This preserves the useful motion without accepting the continuity error.

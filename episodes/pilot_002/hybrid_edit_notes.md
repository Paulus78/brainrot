# Pilot 002 — hybrid edit strategy

Updated: 2026-09-28 (Europe/Berlin)

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

## Three-tap application

The first Veo candidate did not create three contacts. Bongo waved while the bucket lifted, floated and bounced, directly violating the planted-weight requirement. Two deterministic timing tests proved that locked states can solve the count but also exposed a creative problem: hard cuts feel mechanical, and accurate taps without a reaction still feel flat.

The accepted `taps_03_hybrid_v3.mp4` uses these four frames:

1. `frame_03a_ready_clean.png` — paw separated from the rim and no vibration marks.
2. `frame_03b_tap_contact.png` — fingertips visibly press the near rim while the bucket remains fixed.
3. `frame_03c_reaction_clean.png` — Bongo has withdrawn both paws and leans away after the pause.
4. `frame_03d_reaction_rumble.png` — identical reaction and bucket position with bucket-only vibration marks.

The edit blends the ready/contact states into three distinct pulses centered at approximately 0.33, 0.96 and 1.65 seconds. Their durations increase to communicate small, medium and strong force. A 0.56-second motionless gap follows. Only then does Bongo transition into the startled pose and the vibration marks pulse from approximately 2.80 to 3.33 seconds. The bucket position never changes. The matching audio has three increasing dry impacts, silence and one low plastic rattle.

This is the preferred method for countable repeated contacts: lock the physical states, animate only the intended contact variable, preserve a real pause, then add a delayed character reaction. Do not accept technically countable motion if it still lacks emotional cause and effect.

# Pilot 003 — motion QC log

## Acceptance method

Every raw generation is reviewed at normal speed, half speed and as representative frames. A visually attractive first or last frame is insufficient.

For each attempt record:

- Object/limb path is visible and continuous.
- Motion has anticipation, contact, follow-through and settle where appropriate.
- No crossfade, morph, teleport or unexplained object replacement.
- Character invariants survive the full clip.
- One clear action dominates the scene.
- Audio contains no unwanted dialogue or voice change.
- Verdict: `accepted`, `retry with diagnosed correction`, or `rejected`.

## Shot 01

Attempt 01 — **rejected**. Veo 3.1 Fast, 720p, start/end frames.

- Positive: the corn object moved continuously and Bongo showed usable full-body motion.
- Failure: the start frame introduced a different scene and a banana-corn hybrid, while the old end frame used another composition and object state.
- Diagnosis: incompatible anchors, not insufficient model quality.
- Correction: switch to image-element reference mode using only Bongo's original image; generate two clean variants of a simpler giant-corn-cob action.
- Raw clip: `video_raw/rejected/shot_01_attempt_01_mismatched_frame_pair.mp4`
- Contact sheet: `shot_01_attempt_01_contact.png`

Attempts 02A and 02B — generated together in Veo 3.1 Fast, 720p, Bongo reference-element mode.

- Both: coherent single scene, huge cob readable throughout, real body movement, complete object disappearance.
- 02A: usable alternate; Bongo jumps and lands astride the bucket, but the gag is slightly less direct.
- 02B: **accepted**. Stronger centered composition, clearer suction/hop reaction, clean final bucket hold.
- Accepted raw: `video_raw/accepted/hook_01_reference_variant_b.mp4`
- Alternate raw: `video_raw/alternates/hook_01_reference_variant_a.mp4`
- Contact sheets: `shot_01_attempt_02a_contact.png`, `shot_01_attempt_02b_contact.png`

## Shot 02

Attempts 01A and 01B — generated together in Veo 3.1 Fast, 720p, Bongo reference-element mode.

- Both: continuous body motion, readable wind-up, a single large downward action and a stable final bucket.
- 01A: **accepted**. The bucket bulges before the hit, Bongo's two-arm wind-up is broad, the squash/rebound is much stronger, and the resulting launch is the funnier brainrot beat. A small amount of corn is already visible near the opening, but it functions as a useful visual bridge rather than breaking the story.
- 01B: usable alternate; cleaner bucket shape and one readable action, but noticeably less forceful and less funny.
- Accepted raw: `video_raw/accepted/slam_02_reference_variant_a.mp4`
- Alternate raw: `video_raw/alternates/slam_02_reference_variant_b.mp4`
- Contact sheets: `shot_02_attempt_01a_contact.png`, `shot_02_attempt_01b_contact.png`

## Shot 03

Attempts 01A and 01B — generated together in Veo 3.1 Fast, 720p, Bongo reference-element mode.

- Both: the eruption originates visibly inside the bucket, individual popcorn pieces travel and settle continuously, and Bongo is buried before re-emerging.
- 01A: usable alternate; the geyser is large and funny, but Bongo's blue-sandal area becomes visually confusing near the pile.
- 01B: **accepted**. It has the clearest sequence: one warning pop, Bongo leans in, the fountain expands, he is buried, then he emerges and eats one piece. Character identity and the single-sandal rule remain more legible.
- Accepted raw: `video_raw/accepted/payoff_03_reference_variant_b.mp4`
- Alternate raw: `video_raw/alternates/payoff_03_reference_variant_a.mp4`
- Contact sheets: `shot_03_attempt_01a_contact.png`, `shot_03_attempt_01b_contact.png`

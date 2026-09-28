# Pilot 002 — motion quality review

Updated: 2026-09-28 (Europe/Berlin)

| Prototype | State | Critical gate |
| --- | --- | --- |
| 01 Tooth-PING | PASS — HYBRID V1 | One kernel fully enters bucket by 0.71 s; bare right foot remains bare |
| 02 Banana drop | PASS — HYBRID V1 | One intact banana crosses the rim; clean empty-bucket hold follows |
| 03 Three taps | PASS — HYBRID V3 | Three countable contacts, pause, planted self-rumble and delayed reaction |
| 04 Payoff | UNLOCKED | Eruption must visibly originate inside the same planted bucket |

## Attempt log

### Attempt 01 — Veo 3.1 Lite, 720p, 8 s — REJECT

File: `video_raw/rejected/hook_01_attempt_01_veo_lite.mp4`

- Technical file check: PASS — H.264/AAC, 720 × 1280, 24 fps, exactly 8.0 seconds.
- Immediate visual hook: PASS — the first frame already shows the kernel at the tooth and Bongo recoiling.
- Single-kernel rule: PASS in the sampled frames; no duplicate kernel or premature popcorn appears.
- Rim crossing deadline: FAIL — the kernel is still above the bucket around 1.0 s, reaches the rim around 1.5 s and only disappears later. The required entry by 0.9 s is not met.
- Character footwear lock: FAIL — the initially bare planted right foot gains a second blue sandal during the recovery. Bongo therefore ends with two sandals.
- Tooth lock: PASS in the sampled frames — the single tooth remains attached.
- Silent readability: PARTIAL — the kernel eventually reaches the bucket and Bongo looks down, but the motion is too slow for the intended first-second hook.
- Final verdict: automatic reject. Do not use in the edit and do not unlock Prototype 02.

### Required correction for Attempt 02

- Treat the 8-second Veo duration as a fixed canvas, not a 4-second source.
- Complete the kernel's remaining short fall within the first 0.8 seconds, then hold the result.
- Keep the lifted left foot wearing its one blue sandal and the planted right foot visibly bare for the entire clip.
- Do not let Bongo step, swap feet or place the lifted foot on the floor.

### Attempt 02 — Veo 3.1 Lite, 720p, 8 s — REJECT

File: `video_raw/rejected/hook_01_attempt_02_veo_lite.mp4`

- Technical file check: PASS — H.264/AAC, 720 × 1280, 24 fps, exactly 8.0 seconds.
- Timing: PASS relative to Attempt 01 — the visible kernel clears early enough to create a usable first-second action.
- Footwear lock: PASS — the planted right foot stays bare and only the raised left foot wears the blue sandal.
- Character lock: PASS in sampled frames — tooth, blue eye ring and head peel remain attached.
- Cause-and-effect: FAIL — popcorn is already visible inside the bucket at the beginning, then disappears. The kernel also changes into a hollow popcorn-like form before entering.
- Final verdict: automatic reject because the payoff appears before the ingredient enters and the object morphs.

### Attempt 03 — Veo 3.1 Lite Frames, 720p, 8 s — REJECT

File: `video_raw/rejected/hook_01_attempt_03_frames_veo_lite.mp4`

- Method: locked start frame plus clean looking-down end frame.
- Character lock: PASS — one sandal, one tooth, blue eye ring and attached head peel remain readable.
- Empty-bucket lock: PASS at the end.
- Kernel motion: FAIL — the kernel oscillates across the frame, disappears, reappears and only reaches the rim around two seconds.
- Timing: FAIL — the required entry by 0.9 seconds is not met.
- Final verdict: automatic reject. Endpoint locking improved identity but did not solve small-object trajectory or timing.

### Attempt 04 — Veo 3.1 Lite Frames, 720p, 8 s — REJECT

File: `video_raw/rejected/hook_01_attempt_04_rim_frames_veo_lite.mp4`

- Method: almost identical start/end frames; the only intended difference was one kernel directly above the rim versus no kernel.
- Identity and footwear: PASS in sampled frames.
- Kernel count: FAIL — several corn-like objects appear simultaneously inside the bucket and on the floor.
- Physical continuity: FAIL — the kernel bounces, duplicates and exits the bucket despite the locked empty end frame.
- Final verdict: automatic reject. This confirms that further Veo retries on the same micro-object transfer would repeat a known failure mode.

### Hybrid Hook V1 — deterministic state cut, 720p, 3 s — PASS

File: `video_raw/accepted/hook_01_hybrid_v1.mp4`

- Technical file check: PASS — H.264/AAC, 720 × 1280, 24 fps, exactly 3.0 seconds.
- Immediate visual hook: PASS — the first frame is already the tooth-impact state with the kernel visible.
- Single-kernel rule: PASS — one kernel at the tooth, one matching kernel at the rim, then none.
- Entry deadline: PASS — the kernel is fully absent from the open bucket confirmation state by 0.71 seconds.
- Premature payoff: PASS — no popcorn appears.
- Character continuity: PASS — tooth, blue eye ring, attached head peel and exactly one left blue sandal remain present; the planted right foot remains bare.
- Silent readability: PASS — impact, rim approach and empty-bucket confirmation form a clear causal sequence.
- Hold: PASS — the final looking-down state lasts approximately 2.29 seconds.
- Speed policy: PASS — no generated source clip is accelerated.
- Final verdict: accepted and Prototype 02 unlocked.

### Prototype 02 Attempt 01 — Veo 3.1 Lite, 720p, 8 s — REJECT AS RAW

File: `video_raw/rejected/banana_02_attempt_01_veo_lite.mp4`

- Technical file check: PASS — H.264/AAC, 720 × 1280, 24 fps, exactly 8.0 seconds.
- Release readability: PASS — Bongo visibly lets go of the intact banana.
- Rim crossing: PASS — the banana crosses the open rim at approximately 0.6–0.7 seconds.
- Single-banana rule: PASS — no duplicate ingredient banana or popcorn appears.
- Character lock: PASS — head peel, one tooth, blue eye ring and single left sandal remain readable.
- Full disappearance: FAIL — a small brown/yellow stem fragment remains protruding from the back-right interior of the bucket for the rest of the raw clip.
- Final verdict: raw source rejected; only the verified release section is eligible for the hybrid edit.

### Prototype 02 Hybrid V1 — verified motion plus clean hold, 720p, 4.02 s — PASS

File: `video_raw/accepted/banana_02_hybrid_v1.mp4`

- Technical file check: PASS — H.264/AAC, 720 × 1280, 24 fps, approximately 4.02 seconds including AAC frame padding.
- Release and entry: PASS — the unaccelerated Veo motion shows one banana leaving the paw and crossing the rim before 0.71 seconds.
- Clean completion: PASS — the edit cuts before the persistent stem error to `frame_02c_post_drop_clean.png`, where the same bucket is visibly empty.
- Ingredient count: PASS — one banana before entry, none afterward; no popcorn.
- Character continuity: PASS — Bongo retains the attached head peel, one front tooth, blue right-eye ring, one left blue sandal and bare right foot.
- Readable hold: PASS — the empty-bucket confident-grin state holds for more than three seconds.
- Speed policy: PASS — no source footage is accelerated.
- Final verdict: accepted and Prototype 03 unlocked.

### Prototype 03 Attempt 01 — Veo 3.1 Lite, 720p, 8 s — REJECT

File: `video_raw/rejected/taps_03_attempt_01_veo_lite.mp4`

- Technical file check: PASS — H.264/AAC, 720 × 1280, 24 fps, exactly 8.0 seconds.
- Tap count: FAIL — Bongo waves the paw above the rim instead of making three readable contacts.
- Planted-bucket lock: FAIL — the bucket lifts completely off the floor, floats and bounces repeatedly.
- Pause and causality: FAIL — there is no clean sequence of three contacts, stillness and only then self-rumble.
- Character lock: PASS in sampled frames — head peel, eye ring, tooth and single left sandal remain readable.
- Final verdict: automatic reject. The clip repeats the exact hand-held/weightless movement problem this episode was designed to remove.

### Prototype 03 Hybrid V1 — locked-state contacts, 720p, 4.25 s — REJECT

File: `video_raw/rejected/taps_03_hybrid_v1_hard_cuts.mp4`

- Count and bucket position: PASS.
- Motion quality: FAIL — direct state cuts make the paw snap mechanically and recreate the rushed micro-clip feeling.
- Final verdict: useful timing proof only; not accepted.

### Prototype 03 Hybrid V2 — blended contacts, 720p, 4.25 s — REJECT

File: `video_raw/rejected/taps_03_hybrid_v2_no_reaction.mp4`

- Three contacts and increasing force: PASS.
- Pause before rumble: PASS.
- Planted-bucket lock: PASS.
- Entertainment and cause/effect: PARTIAL — Bongo does not react to the self-rumble, so the final beat feels emotionally flat.
- Final verdict: structurally correct but superseded by V3.

### Prototype 03 Hybrid V3 — blended taps, delayed reaction and planted rumble, 720p, 4.25 s — PASS

File: `video_raw/accepted/taps_03_hybrid_v3.mp4`

- Technical file check: PASS — H.264/AAC, 720 × 1280, 24 fps, exactly 4.25 seconds.
- Tap count: PASS — three individually readable paw-to-rim contacts occur at increasing visual durations.
- Contact separation: PASS — the paw fully leaves the rim between all three contacts.
- Comedy pause: PASS — more than half a second of complete stillness follows the strong third tap.
- Self-rumble: PASS — vibration marks and the low rattle begin only after the pause.
- Planted-bucket lock: PASS — the bucket never slides, tilts, lifts or enters Bongo's hands.
- Character continuity: PASS — head peel, one tooth, blue right-eye ring, one left sandal and bare right foot remain present.
- Reaction: PASS — Bongo retracts both paws and leans away only after the bucket begins to rattle.
- Audio structure: PASS — three dry taps grow in force, followed by silence and one low rattle; no dialogue or music.
- Final verdict: accepted and Prototype 04 unlocked.

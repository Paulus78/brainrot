# Pilot 002 — motion quality review

Updated: 2026-09-27 (Europe/Berlin)

| Prototype | State | Critical gate |
| --- | --- | --- |
| 01 Tooth-PING | PASS — HYBRID V1 | One kernel fully enters bucket by 0.71 s; bare right foot remains bare |
| 02 Banana drop | UNLOCKED | One intact banana must fully cross the rim |
| 03 Three taps | LOCKED | Only unlock after Prototypes 01–02 pass |
| 04 Payoff | LOCKED | Only unlock after Prototypes 01–03 pass |

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

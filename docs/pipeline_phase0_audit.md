# Bongo Bucket pipeline — Phase 0 audit

Updated: 2026-09-29 (Europe/Berlin)

## Scope

This audit evaluates the repository against the user-supplied pipeline brief `codex prompt bongo bucket.md`. The brief is treated as a design source, not as authority that overrides the current project evidence. No production pipeline code is added in Phase 0.

## Executive decision

The repository contains useful creative history and several good low-level utilities, but it is not a production pipeline. It is a collection of episode-specific scripts, manually named files and narrative QC documents. The strongest parts of the supplied brief should become the new architecture:

- one validated storyboard file as the source of truth;
- deterministic ingest, media checks, assembly and logging;
- a separate generator and judge role;
- explicit failure classes and a maximum of three attempts;
- fixed voice/SFX assets instead of Veo audio;
- human gates before expensive generation and before export.

However, three rules from the supplied brief must be changed because they reproduce failures already demonstrated by Pilots 001–003:

1. `One character, one action, static camera` is retained, but **four-second independent shots are not the default**.
2. `Use only the best 1–3 seconds and cut fast` is rejected as a global rule. Cut duration follows action readability.
3. Start/end frames are not automatically generated for every shot. Continuations must prefer a real end frame or Flow **Extend** from the accepted parent clip.

## Existing project audit

### Keep as active foundations

| Asset | Decision | Reason |
| --- | --- | --- |
| `assets/character_master/bongo_reference.png` | Keep | Only current canonical character source. |
| `episodes/pilot_002/audio/accepted/voice_master_v1.wav` | Keep provisionally | Contains the only measured, internally consistent `Bucketo.` / `Bongo snacko.` performance. It is not a complete catchphrase library. |
| `src/edit/analyze_voice.py` | Keep and generalize | Reusable deterministic pitch/level analysis; already independent of episode layout. |
| ffmpeg discovery logic | Keep once, centralize | Repeated in several scripts and proven on this machine. |
| Historical accepted/rejected clips and QC | Keep as calibration corpus | Essential examples for future human labels and judge calibration. |
| Maximum three attempts per shot | Keep | Prevents prompt-tuning loops and uncontrolled credit spend. |
| One primary action per generated unit | Keep | Best observed defense against Veo action confusion. |
| Git history and explicit rejected states | Keep | Allows recovery and honest comparison. |

### Replace or redesign

| Current component | Problem | Replacement |
| --- | --- | --- |
| `schemas/episode.schema.json` | Requires exactly four `pilot_###` shots and caps the episode at 15 s; it does not model continuity, attempts, candidate clips, audio cues or failure classes. | Versioned storyboard schema with flexible shot count, continuity groups, `extends`, start/end state, generation policy, audio cue IDs and judge gates. |
| Episode-specific `compose_*.py` and `build_*.sh` | Hardcoded file paths, timings, source audio and output names. | One data-driven assembler that consumes validated storyboard plus an edit decision file. |
| Native audio concatenation | Produced unrelated room tones and effects at every cut. | Discard Veo audio by default; assemble room tone, Foley, SFX, music and voice from separate assets. |
| Contact sheets as primary clip review | Cannot judge motion rhythm, audio or cut continuity. | Contact sheets remain diagnostic only; real-time playback and boundary-frame inspection are hard gates. |
| Free-form prompt documents | No machine-readable relationship between prompt, reference, attempt and verdict. | Job manifests plus SQLite attempt log. |
| Manual ad-hoc downloads | Files are renamed and organized after the fact. | `flow_jobs/` manifests and strict `inbox/<job_id>__candidate_<n>.mp4` ingest convention. |
| Current README | Stops at Pilot 002 and describes old one-off commands as the workflow. | Rewrite after MVP CLI and directory contract exist. |
| `config.example.yaml` | Contains stale pricing/model facts and an unconfirmed TTS API route. | Provider-neutral local config with verified capabilities recorded per run, never as permanent truth. |

### Preserve only as historical evidence

These files should not be deleted because they document failures and can train/calibrate later review. They must not be called by the new production path:

- `src/edit/build_taps_hybrid.sh`
- `src/edit/build_payoff_hybrid.sh`
- `src/edit/build_picture_cut.sh`
- `src/edit/compose_animatic.py`
- `src/edit/compose_pilot_002_animatic.py`
- `src/edit/compose_v2_animatic.py`
- `src/edit/compose_final.py`
- `src/edit/compose_v2_final.py`
- `src/edit/build_episode_002_final.sh`
- `src/edit/build_episode_003_final.sh`

They are episode artifacts, not reusable architecture.

## Supplied brief: accepted, modified and rejected rules

### Accepted

- Deterministic Python state machine.
- No multi-agent production pipeline.
- Storyboard JSON validated before downstream work.
- Cheap still checks before video credits.
- Manual Flow handoff through files rather than invented API capabilities.
- Generator and judge separated conceptually.
- Hard gates plus coarse soft scores.
- Pairwise comparison for multiple candidates.
- Failure classes and one-change-per-retry discipline.
- Maximum three generations per unit.
- SQLite attempt/cost log.
- Small playbook derived from measured results.
- No publishing or ML training in the MVP.

### Modified

- **Shot duration:** no fixed 4 s. Default generation unit may be 4–8 s; edit duration is selected from readable action beats.
- **Cutting:** no mandatory 1–3 s extraction. A clip may run longer when anticipation and payoff need it.
- **Frames:** a manually approved canonical first frame is useful; an end frame is allowed only when it depicts the same verified composition. Otherwise use the real last frame of the parent clip or Flow Extend.
- **Judge:** automatic vision scoring is untrusted until compared with at least 40 human labels. Until then it can flag, never finally approve.
- **Keyframes:** generate one canonical world/continuity frame first. Per-shot keyframes are optional, not mandatory.
- **Character consistency:** embedding similarity is only a warning signal because a high similarity score can coexist with wrong sandal, tooth or eye-ring state.

### Rejected

- A default chain of all legacy catchphrases in every episode. It creates too much dialogue and repeats the voice-consistency problem.
- Multiple visual twists as a requirement. One clear escalation and one twist are safer and funnier than several poorly connected reveals.
- Native Veo dialogue or native Veo audio in the final mix.
- Fast cutting as a substitute for continuity.
- Hiding difficult causal events behind flashes by default. This is allowed only when the story remains understandable without sound.
- `subtitles: true` as a default. The current format is designed to be visually international; subtitles remain an episode-level choice.

## Required V1 architecture

```text
bongo_pipeline/
  cli.py                  # state-machine commands
  config.py               # local configuration loading
  schema.py               # storyboard/job validation
  project.py              # paths and episode state
  flow_jobs.py            # deterministic manual Flow handoff
  ingest.py               # filename mapping and ffprobe gates
  judge.py                # manual/automatic verdict contract
  continuity.py           # boundary frames and state checks
  assemble.py             # picture-only and final export
  audio.py                # cue-sheet/stem assembly, never Veo bed
  store.py                # SQLite runs, attempts and verdicts
schemas/
  storyboard.v1.schema.json
  flow_job.v1.schema.json
tests/
  fixtures/
  test_schema.py
  test_ingest.py
  test_state_machine.py
assets/
  characters/
  props/
  envs/
  audio/voice/
  audio/sfx/
  audio/music/
  loops/
  reactions/
  vfx/
flow_jobs/
inbox/
```

## State machine proposal

```text
IDEA_SELECTED
  -> STORYBOARD_VALIDATED
  -> CANONICAL_FRAME_APPROVED
  -> FLOW_JOBS_READY
  -> CLIPS_INGESTED
  -> CLIPS_JUDGED
  -> PICTURE_LOCKED
  -> AUDIO_BUILT
  -> FINAL_REVIEWED
  -> COMPLETE
```

A failed judge returns the unit to `FLOW_JOBS_READY` with exactly one logged `failure_class`. Exceeding three attempts moves the unit to `REWRITE_REQUIRED`, not another retry.

## Continuity model missing from the supplied schema

Every generated unit needs these additional fields:

```json
{
  "continuity_group": "garage_take_01",
  "parent_clip_id": null,
  "generation_mode": "base",
  "start_state": {},
  "end_state": {},
  "must_match": ["camera", "environment", "bucket", "bongo_identity"],
  "audio_policy": "discard_native"
}
```

An extension changes `generation_mode` to `extend` and sets `parent_clip_id`. Independent shots may share a continuity group only when their boundary states are explicitly compatible.

## MVP boundaries

Phase 1 should build only:

1. storyboard/job schemas and validation;
2. episode state file;
3. deterministic Flow job export;
4. deterministic clip ingest with duration/resolution/audio inspection;
5. manual judge JSON with hard gates and failure classes;
6. SQLite logging;
7. picture-only ffmpeg assembly from explicit trims;
8. separate audio cue/stem assembly contract;
9. tests for schema, ingest and state transitions.

It should not generate images, call a paid video API, control Flow, create a vision-model judge, build embeddings, or auto-publish.

## Resolved defaults for Phase 1

These choices can be made from existing evidence without blocking on questions:

- Default episode target: 15 s, configurable per storyboard.
- Default subtitles: off.
- Default video audio policy: discard native audio.
- Default candidate count: two for a base clip, two extensions for the selected base.
- Default review authority: human until an automatic judge is calibrated.
- Default continuity strategy: canonical base clip plus extension, not independent clips.
- Existing voice master may be imported as a provisional asset but no missing catchphrases are synthesized in MVP.

## Open decisions that do not block implementation

1. Which external vision model, if any, will later be used for the automatic judge?
2. Should future human-label calibration live in a minimal local web page or a command-line review queue?
3. Should the active format keep only `Bucketo.` and `Bongo snacko.`, or will a new complete voice pack be supplied later?

## Phase 0 conclusion

Proceed to Phase 1 with a small local pipeline core. Do not generate another video before the storyboard schema, continuity group, manual Flow job, ingest gates and picture-only review path exist. The immediate next implementation target is a fully tested round trip:

`storyboard.json -> validate -> flow_jobs/ -> inbox/ -> ingest -> manual verdict -> picture-only assembly`.

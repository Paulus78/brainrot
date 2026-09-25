# Production status — pilot_001

Updated: 2026-09-25 (Europe/Berlin)

## Completed

- Repository/reference review
- Safe runtime and credential presence check; no provider secrets were printed
- Current official OpenAI image, video and TTS documentation review
- Character master copied into the writable project
- Episode manifest and JSON Schema
- Final four-shot decomposition
- Keyframe prompts, video motion prompts and audio cue sheet
- Keyframes accepted for Shots 01, 03 and 04
- Google Flow project created: `Bongo Bucket – pilot_001`
- Flow image mode verified at 0 credits per image
- Voice Auditions A/B/C exported as WAV with the identical audition script
- 12-second vertical animatic exported as GIF/WebP with exact 2s / 2s / 3s / 5s shot timing; Shot 02 is visibly marked as pending
- Shot 04 Veo attempt 01 rejected for character drift
- Shot 04 Veo attempt 02 accepted as a motion base with a minor-drift warning
- Flow custom Bongo voice created from the Algieba preset with warm, lightly raspy, slightly nasal and dry performance direction
- Shot 02 keyframe generated in Flow at 0 credits and accepted after identity/action QC
- Shot 02 animated with the natural Flow custom voice and accepted after visual/action QC
- Shot 01 animated with the Flow custom voice and accepted after visual/identity QC
- Shot 03 custom-voice attempt 01 rendered and retained as a clean fallback; motion QC is WARN because the three shake beats are not distinct enough
- All currently downloaded raw video files are stored in the repository-ready project structure

## Pending

- Final listening comparison for the Flow custom-voice renders; all local system-voice prototypes remain rejected as too robotic
- Produce and review a stronger Shot 03 take with three clearly separated shake beats
- Mix and edit
- Apply final quality gates and write the postmortem

## Current constraints

- Local runtime has Python 3.8.4 but no `ffmpeg` or `ffprobe`; macOS `avconvert` is available for trimming/transcoding.
- No `OPENAI_API_KEY`, `GOOGLE_API_KEY`, `GEMINI_API_KEY` or `ELEVENLABS_API_KEY` is configured.
- The OpenAI Sora Videos API was shut down on 2026-09-24 and has no one-to-one replacement API.
- Flow currently charges 4 credits for one 4-second 360p clip in the active project.
- Twenty-four Flow credits have been used so far: two Veo motion attempts, one Omni custom-voice attempt for Shot 04, accepted Omni renders for Shots 01 and 02, and the first Shot 03 Omni take.

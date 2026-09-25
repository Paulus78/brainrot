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
- Shot 03 custom-voice attempt 01 retained as a clean fallback; motion QC is WARN because the three shake beats are not distinct enough
- Shot 03 custom-voice attempt 02 accepted: three distinct progressively stronger bucket shakes and a centered end pose
- Shot 04 custom-voice attempt 03 rejected for final because it omits “OOOOOO… perfecto.”
- Shot 04 custom-voice attempt 04 accepted: stable banana-propeller motion and both scripted voice beats
- Final 12-second H.264/AAC pilot assembled at 360 × 640 with restrained original bucket hits, reveal sting and fan-air layer
- Final technical and visual quality gates passed; no black frames or clipping detected
- Reproducible final edit script added at `src/edit/compose_final.py`
- All currently downloaded raw video files are stored in the repository-ready project structure

## Pending

- Human listening pass on the assembled MP4 before any public upload
- Optional 720p upscale only after the voice performance is approved by ear

## Current constraints

- The final edit uses an existing local `ffmpeg` binary discovered inside Streamlabs OBS; on another computer install `ffmpeg` or set the `FFMPEG` environment variable.
- No `OPENAI_API_KEY`, `GOOGLE_API_KEY`, `GEMINI_API_KEY` or `ELEVENLABS_API_KEY` is configured.
- The OpenAI Sora Videos API was shut down on 2026-09-24 and has no one-to-one replacement API.
- Flow currently charges 4 credits for one 4-second 360p clip in the active project.
- Thirty-two Flow credits were used: two Veo motion attempts, two Omni custom-voice attempts for Shot 04, accepted Omni renders for Shots 01 and 02, and two Shot 03 Omni takes.

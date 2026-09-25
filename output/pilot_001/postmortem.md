# Postmortem — pilot_001

## Outcome

The pilot reached a complete 12-second final candidate with all four shots, embedded custom voice, original sound accents and a reproducible local edit. The banana-as-propeller payoff is immediately readable and the accepted shots preserve Bongo’s core identity.

## What worked

- Using the supplied Bongo image as the hard visual identity reference kept the blue eye ring, single tooth, head banana and one blue sandal recognizable.
- Short, single-action prompts were more stable than prompts asking for complex body motion.
- Flow’s custom Algieba-based voice was materially more suitable than the three rejected local system-voice auditions.
- The second Banga take succeeded after the motion was specified as three timed, separated amplitudes with a full return to center.
- The fourth reveal take succeeded after both dialogue lines, the silent beat and all locked visual features were stated explicitly.
- Keeping every raw attempt and its QC decision makes the project recoverable on another computer.

## What needed iteration

- Reveal attempt 01 had unacceptable face, arm and head-banana drift.
- Reveal attempt 02 was visually usable but silent and still had minor drift.
- Reveal attempt 03 looked stable but omitted “OOOOOO… perfecto.” because the prompt contained only the final line.
- Banga attempt 01 was too subtle; the shake amplitudes did not read clearly.
- The original 2-second Shot 01 allocation would have cut off the last spoken beat. The final edit uses the allowed 2.5-second maximum and compensates with a 4.5-second reveal, preserving the 12-second total.

## Final editorial choices

- Timing: 2.5 s / 2.0 s / 3.0 s / 4.5 s.
- Hard cuts preserve the fast brainrot rhythm and avoid transition artifacts.
- A 0.5-second final hold lets “Bongo fixo.” land without rushing.
- Three low synthetic bucket hits reinforce the ritual without competing with voice.
- A very short two-note original sting and filtered fan air support the reveal; there is no continuous melody.

## Cost and reproducibility

- Flow image generation was verified at 0 credits for the used keyframe workflow.
- Eight 4-second 360p video generations at 4 credits each used 32 Flow credits.
- Raw inputs, prompts, QC notes, the final MP4 and the composition script are stored in the repository.
- On a different computer, install `ffmpeg`, clone the repository and run `python3 src/edit/compose_final.py` to rebuild the final cut.

## Next episode improvements

- Lock one canonical workshop background plate for tighter inter-shot continuity.
- Put every required line into a single source-of-truth prompt block before generation.
- Generate 5–6 second reveal sources when available so the final dry beat has more natural tail room.
- Add a human listening checkpoint immediately after the first custom-voice render, before spending credits on all shots.

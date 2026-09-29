# Pilot 003 postmortem and production process V4

Updated: 2026-09-29 (Europe/Berlin)

## Decision

`output/pilot_003/pilot_003_bananacorno_v1.mp4` is **rejected**. It contains better motion inside the individual clips than Pilot 002, but it does not work as one video. The visual continuity breaks at both edits and the automatically generated sound beds do not form a coherent soundtrack.

This is a process failure, not a small polish problem. Do not spend more credits on independent replacement clips and do not try to hide these joins with transitions.

## What failed in the picture edit

### Cut 1, approximately 6.02 seconds

Before the cut, Bongo is in a frontal close-up with both paws on a small bucket. After the cut, he is shown much wider and from the side. The bucket instantly gains a large handle and is suddenly full of visible kernels. The garage layout, lens, scale, lighting and Bongo's pose all reset at once.

The viewer therefore does not read a time cut. The viewer reads a replacement scene.

### Cut 2, approximately 12.50 seconds

Before the cut, Bongo stands proudly next to a clean, apparently empty bucket. After the cut, the camera becomes frontal, the garage changes again, the handle moves across the bucket face, popcorn is already scattered on the floor and one piece is already in the air.

This removes the suspense beat and makes the eruption appear to have started off-screen. The cause-and-effect chain is interrupted precisely where the payoff should become clearest.

Audit frames are stored in `episodes/pilot_003/qc/cut_audit/`.

## What failed in the sound edit

The three Veo clips each contain their own complete native audio generation. Those tracks were trimmed, mildly sped up, concatenated and then loudness-normalized. That was the wrong source strategy.

- Each clip has a different room tone, frequency balance and cartoon-Foley vocabulary.
- The sound changes at the same instant as the large visual resets, making each edit feel even harder.
- The mean level in the one-second window after cut 2 is about 5.7 dB lower than the preceding one-second window.
- Global loudness normalization raises unrelated ambience and artifacts together with useful effects; it cannot repair timing or semantic mismatch.
- The final voice line was mixed over the generated payoff soundtrack without a deliberately designed ambience, Foley and voice hierarchy.
- No cue sheet was created before the mix, and no separate ambience, hard-effect, Foley and voice stems existed.

Adobe's current sound-design guidance distinguishes ambience from isolated effects and Foley, requires hard effects to synchronize to the visible action, and recommends fades on soundtrack elements. It also recommends building effects in layers rather than treating one generated clip track as a finished mix. Adobe's J/L-cut guidance describes overlapping audio across visual edits to preserve continuity. The Pilot 003 edit did neither.

## What failed in review

The largest mistake was accepting clips independently.

- Contact sheets were used to select attractive motion, but a contact sheet cannot judge rhythm, sound or the perceptual violence of a cut.
- The edit was assembled from fixed time ranges instead of hand-selected action and reaction beats.
- Known continuity errors were described as acceptable before the full sequence passed a real-time review.
- Technical checks such as resolution, loudness and black-frame detection were mistaken for creative quality.
- The final review did not enforce three separate passes: picture only, audio only and complete playback.
- `good enough` was interpreted as permission to accept broken continuity. It should only allow small texture defects after story, timing and sound already work.

## Research conclusions

Google's current Veo 3.1 documentation provides the missing continuity tool: scene extension uses the last second of the previous shot to continue the story while preserving visual and audio consistency. Google Flow also allows frames from generated video to be saved as ingredients or start frames, and its Scenebuilder is intended for trimming and previewing sequences.

YouTube's current Shorts guidance emphasizes a hook within the first second and describes successful Shorts as compact individual moments with a simple mini-story. The relevant lesson is not to cut faster. It is to reduce the idea until one continuous moment can carry shock, intrigue and payoff.

Brainrot's useful qualities are an instantly legible absurd character/object combination, a repeatable signature and nonsensical humor. Random continuity errors and unrelated sounds are not part of the format; they merely make the video harder to understand.

## Production process V4

### 1. Lock one canonical world before video generation

Create and approve one 9:16 reference frame containing the exact Bongo, one exact bucket and one exact garage angle. Record a small continuity bible: bucket size and handle position, camera height, lens/framing, Bongo's left sandal and all fixed background landmarks.

Do not generate video until this one frame reads correctly on a phone screen.

### 2. Reduce the episode to one continuous moment

Use one static camera and only these beats:

1. Giant cob is already jammed into the bucket; Bongo pushes immediately.
2. The bucket swallows it and bulges.
3. Bongo performs one slam and waits.
4. The bucket erupts; Bongo emerges and eats one piece.

No separate ingredient scene, no repeated ritual and no new camera setup.

### 3. Generate one base clip, then extend it

- Generate Part A as one 8-second clip from the approved canonical frame or ingredients.
- Select by real-time playback, not contact sheet alone.
- Continue the selected clip with Flow's **Extend** function. The final second of Part A becomes the visual and acoustic anchor for Part B.
- Generate two extensions of the same accepted base clip and select the better continuation.
- Never rebuild Part B independently from the Bongo portrait.

Target shape:

- Part A, 0–8 s: push, suction, bulge, one slam, short wait.
- Extension, approximately 8–15 s: eruption, burial, emergence, bite and hold.

This requires two linked generations, not three unrelated generations.

### 4. Lock picture with all generated audio muted

Build and review the complete sequence silently at normal speed. A shot passes only when:

- The 12 frames before and after every edit or extension preserve camera, pose, bucket geometry and object state.
- No ingredient or result appears before its cause.
- Every action has anticipation, contact, follow-through and a readable reaction.
- The first second contains the absurd problem, and the final gag holds for at least one second.

If picture continuity fails, reject the generation. Do not hide it with a dissolve, speed ramp, crop or loud sound.

### 5. Rebuild sound from zero after picture lock

Mute all Veo native audio in the final edit. Create one cue sheet with exact frame/time references and separate tracks:

- one continuous low garage room tone across the entire episode;
- effort squeaks tied to Bongos body motion;
- one suction sound that peaks when the cob disappears;
- one low bucket bulge/rumble;
- one slam impact exactly on palm contact;
- 6–10 frames of near-silence before the eruption;
- one escalating popcorn burst with individual falling impacts;
- one bite/crunch;
- one final voice line from a single voice master.

Use short fades on every element and J/L-style overlap for ambience. Duck effects under the voice instead of normalizing the whole mixture into one dense block.

### 6. Mandatory review order

1. **Silent picture pass:** story and continuity only.
2. **Audio-only pass:** no visual assistance; ambience, effects and voice must form one coherent arc.
3. **Full-speed pass on phone-sized preview:** rhythm and comedy.
4. **Two cut-boundary inspections:** last 12 frames versus first 12 frames.
5. **Technical pass:** format, loudness, peaks and black frames.

The master remains `REJECTED` until all five pass. Technical correctness can never override a failed creative pass.

### 7. Credit and retry policy

- One approved canonical still before spending video credits.
- Two variants for the base clip.
- Two extensions from the selected base clip.
- One additional retry only when the exact failed motion or continuity defect is written down.
- No audio generation or mix work before picture lock.

This is both cheaper and safer than generating three independent scenes, because a failed base clip is discovered before dependent work begins.

## Recommended next action

Do not repair Pilot 003 V1. Rebuild it as one base clip plus one extension, with native audio muted. Before generating, prepare one canonical 9:16 Bongo/bucket/garage frame and review it against the continuity bible.

## Sources

- Google DeepMind, Veo 3.1 capabilities and scene extension: https://deepmind.google/models/veo/
- Google DeepMind, Veo prompt guide: https://deepmind.google/models/veo/prompt-guide/
- Google Flow Help, editing, extension and Scenebuilder: https://support.google.com/labs/answer/16935718?hl=en
- Google Flow Help, ingredients and frames: https://support.google.com/flow/answer/16353334?hl=en
- YouTube Blog, Shorts hook and mini-story guidance: https://blog.youtube/creator-and-artist-stories/youtube-shorts-deep-dive/
- YouTube Blog, Italian brainrot trend analysis: https://blog.youtube/culture-and-trends/trending-now-june-2025/
- Adobe, sound-effect categories, synchronization and layering: https://www.adobe.com/creativecloud/video/discover/sfx-for-video.html
- Adobe Premiere, J and L cuts: https://helpx.adobe.com/ie/premiere/desktop/edit-projects/trim-clips/perform-j-cuts-and-l-cuts.html

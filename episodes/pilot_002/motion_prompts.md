# Pilot 002 — Veo motion prompts

All motion renders are vertical 9:16 and use the accepted storyboard frame for that beat. Generate one candidate at a time and apply its quality gate before moving on. Do not generate final dialogue in any video render.

## Prototype 01 — Tooth-PING hook

Start image: `keyframes/frame_01_tooth_ping.png`

Target source length: 4 seconds. Intended final use: approximately 2.5–3.0 seconds without acceleration above 1.15×.

### Veo prompt

Animate this exact accepted 9:16 storyboard frame as one continuous, immediately readable comic action. Preserve Bongo's identity absolutely: same light-brown shaggy fur, enormous ears, asymmetric eyes, vivid cobalt-blue ring around the smaller right eye, exactly one firmly attached front tooth, same banana peel on his head and exactly one blue sandal on his left foot. Preserve the exact same yellow smiley bucket and warm garage.

Begin at the instant just after the hard kernel has struck the tooth. At 0.0 seconds, play one crisp nonverbal PING. The single visible golden corn kernel continues along its existing downward trajectory, crosses the open yellow bucket rim by 0.7 seconds and disappears completely inside by 0.9 seconds. Do not create another kernel. Bongo makes one quick physical recoil: his lifted foot and both ears react, but he does not fall. His front tooth remains firmly attached, motionless and unchanged. Immediately after the kernel disappears, Bongo's eyes and head follow downward toward the bucket. He freezes in confused silence for the rest of the clip so the cause and destination remain clear.

Keep the camera almost locked. A tiny downward ease following the existing kernel path is allowed only if the open rim, Bongo's face and the blue eye ring remain visible. Preserve natural weight and smooth 24 fps motion. Generate only the PING, a small bucket plink and subtle fur movement; no speech, music or vocalization.

No cut, zoom burst, camera spin, new object, second kernel, loose tooth, tooth bend, missing tooth, second bucket, whole banana, popcorn, text, subtitle, duplicated limb, disappearing blue ring, changed sandal, detached head peel, morph or teleportation.

### Hard acceptance gate

The hook passes only if every item is true:

- One and only one kernel is visible throughout its flight.
- The kernel crosses the bucket rim and fully disappears by 0.9 seconds.
- The tooth never moves independently, bends, duplicates or detaches.
- The blue eye ring, head peel and single left sandal remain unchanged.
- The action is understandable with audio muted at normal playback speed.
- The first frame already contains action; there is no establishing delay.
- Bongo's reaction is lively but does not obscure the kernel or bucket.
- The final looking-down hold lasts at least 1.5 seconds in the four-second source.

### Automatic rejection reasons

- Kernel misses the bucket, bounces out or becomes popcorn early.
- Additional kernels or ingredients appear.
- Tooth damage becomes the story instead of a harmless comic PING.
- Bongo changes species, eye layout, footwear or head banana.
- Camera motion hides the bucket crossing.
- A voice, word, caption or musical sting is generated.
- The clip requires acceleration above 1.15× to fit the edit.

### Corrective retry prompt after Attempt 01

Animate this exact 9:16 input frame for eight seconds. The input image is the identity and layout lock. Do not redesign anything.

MOST IMPORTANT ACTION, FIRST 0.8 SECONDS ONLY: the one golden kernel already visible directly below Bongo's tooth immediately continues straight down along the drawn motion trail. It crosses the clearly visible bucket rim before 0.6 seconds and is completely hidden inside the bucket before 0.8 seconds. This is a very short, fast fall, not a slow float. There is exactly one kernel. It never touches the rim, never bounces and never returns.

Bongo's body performs only a tiny recoil in place. His raised LEFT foot stays raised for the whole clip and keeps the only blue sandal. His planted RIGHT foot stays planted, completely bare and brown for the whole clip. Never add footwear to the right foot. Never put the raised foot down, never step, never swap the feet and never duplicate the sandal. His ears make one small delayed flap. His one front tooth remains rigidly attached and unchanged.

From 0.8 to 1.6 seconds, Bongo's pupils and head snap downward to the bucket. From 1.6 seconds to the end, he holds a confused stare into the bucket with only subtle breathing and fur settling. The bucket never moves. Keep the static eye-level camera and the full open rim visible continuously.

Audio: exactly one short metallic PING at the first frame and one quiet bucket plink before 0.8 seconds. No voice, speech, words, singing, music or extra sound gag.

Forbidden: a second kernel, popcorn, banana ingredient, closed bucket, rim collision, slow-motion falling, camera movement, crop change, missing blue eye ring, eye redesign, tooth movement, tooth loss, two sandals, shoe material appearing on the bare right foot, walking, foot swap, duplicated limb, detached head peel, text, subtitle, cut, morph or teleportation.

Retry acceptance gate: kernel completely hidden by 0.8 seconds; raised left foot still has one blue sandal; planted right foot remains fully bare in every sampled frame; tooth, eye ring and head peel remain unchanged; no speech; at least 1.5 seconds of readable looking-down hold is available.

## Prototype 02 — Banana drop

Unlocked after the accepted Hybrid Hook V1.

Start image: `keyframes/frame_02_banana_drop.png`

Animate one continuous release. The exact one whole ingredient banana leaves Bongo's paw, crosses the open rim and fully disappears inside the same planted yellow bucket. Bongo's head peel remains attached and unchanged. The hidden kernel stays hidden. Bongo ends with the same confident crooked grin and looks into the bucket. Camera almost locked; no dialogue, extra banana, popcorn, bucket movement, cut, morph or teleportation.

Motion gate: paw visibly releases one banana; the whole ingredient crosses and clears the rim without the stem remaining visible.

### Production note after hook tests

Prototype 01 proved that Veo is unreliable for tiny rigid-object transfers even with locked endpoints. For Prototype 02, generate one carefully scoped candidate because the banana is larger and easier to track. If the banana duplicates, morphs, reverses direction or remains visible after crossing the rim, reject immediately and use a locked release / rim / empty-bucket state sequence instead of repeating the same prompt.

## Prototype 03 — Three taps and self-rumble

Unlocked after accepted Hybrid Hook V1 and Banana Drop Hybrid V1.

Start image: `keyframes/frame_03_planted_bucket_tap.png`

The bucket remains heavy and flat on the floor. Reconstruct exactly three separated one-paw taps with increasing force: small, medium, strong. The tapping paw clearly leaves the bucket between contacts; the other paw stays close to Bongo's body. After the third tap, hold complete stillness for half a second. Only then the bucket rumbles by itself without sliding, tilting or lifting. Bongo leans back and takes one cautious half-step. No hand-held shake, no dialogue, no popcorn, no escaping ingredient, no camera shake.

Motion gate: three contacts are individually countable and the bucket's self-rumble begins only after the pause.

### Production result

The direct Veo attempt failed because the paw waved without three contacts and the bucket floated and bounced. Repeating the same generation would reproduce a known failure mode. The accepted `taps_03_hybrid_v3.mp4` therefore uses four continuity-locked states: clean ready pose, unmistakable rim contact, clean startled reaction and the same reaction with bucket-only vibration marks. Three smoothly blended contact pulses increase in duration, a 0.56-second still pause follows, then the vibration marks pulse while the bucket remains pixel-locked to the floor. Three rising dry taps, silence and a low rattle reinforce the same structure. Prototype 04 is unlocked.

## Prototype 04 — Banana-popcorn payoff

Unlocked after Hybrid Hook V1, Banana Drop Hybrid V1 and Three Taps Hybrid V3.

Start image: `keyframes/frame_04_banana_popcorn_payoff.png`

Use the frame as the intended final state. Create a short wide payoff in which a fountain of small fluffy banana-shaped popcorn finishes erupting from the visible yellow bucket and settles around Bongo. Do not recreate the whole transformation offscreen. Bongo remains buried to his neck, raises exactly one snack piece, takes a small satisfied bite and ends in the exact stable dry-proud pose. Allow one gentle camera pullback only. Hold the final composition at least 1.5 seconds. No final dialogue, second bucket, whole flying bananas, fire, duplicate Bongo, missing blue ring, loose tooth or obscured face.

Motion gate: the eruption visibly originates from the bucket, Bongo's face remains readable and the final hold is long enough to understand the joke.

### Production result

Chrome/Flow was retried, but its upload control repeatedly opened unrelated media or returned to the Flow home screen. The payoff therefore uses the already proven locked-state method rather than spending more credits behind an unreliable UI path. `frame_04a_eruption_start.png`, `frame_04b_eruption_mid.png` and `frame_04c_payoff_hold.png` share the same camera and bucket position. Hybrid V1 proved the structure but was rejected because long dissolves caused visible ghosting. Accepted `payoff_04_hybrid_v2.mp4` confines each growth transition to 0.30–0.35 seconds, then holds the settled mound and snack pose from about 1.45 to 5.0 seconds. The audio uses only dry popcorn pops, a low eruption whoosh and one final crunch. No dialogue is embedded.

## Final voice policy

Only after the picture edit passes the silent-story review, create both lines in one uninterrupted session with one locked voice:

1. “Bucketo.” — brief, self-assured, warm mid-low register.
2. “Bongo snacko.” — dry, satisfied, identical register and character.

Do not direct surprise through a higher pitch. Use timing, breath and a slight pause instead.

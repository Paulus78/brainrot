# Video QC — pilot_001

## Shot 01 — problem

| Attempt | Route | Result | Notes |
|---|---|---|---|
| 01 | Omni Flash, ingredients, custom Bongo voice, 360p, 4 s | PASS | Clear puzzled head tilt and eye movement; fan stays completely off; exact blue eye ring, tooth, head banana, single left sandal, bucket, fan, framing and workshop remain stable. Custom voice is embedded with the exact line “Bongo… no no no.” |

## Shot 02 — Bucketo

| Attempt | Route | Result | Notes |
|---|---|---|---|
| 01 | Omni Flash, ingredients, custom Bongo voice, 360p, 4 s | PASS | Exactly one banana is lowered into the bucket; fan remains off; blue eye ring, tooth, head banana, single left sandal, bucket, framing and background remain stable. Natural custom voice says “Bucketo.” |

## Shot 03 — Banga

| Attempt | Route | Result | Notes |
|---|---|---|---|
| 01 | Omni Flash, ingredients, custom Bongo voice, 360p, 4 s | WARN / fallback only | File and visuals are technically clean; Bongo, bucket, sandal, head banana, camera and workshop remain stable. The three requested shake beats are too subtle to read as clearly separated small / medium / strong actions, so a stronger second take is required. |
| 02 | Omni Flash, ingredients, custom Bongo voice, 360p, 4 s | PASS | Three distinct beats are visible: small first tilt, a returned center beat, medium second tilt, then a clearly stronger third tilt; the bucket returns centered by 3.12 s. Feet, camera, face design, head banana, blue eye ring, sandal and workshop remain stable. |

## Shot 04 — reveal

| Attempt | Route | Result | Notes |
|---|---|---|---|
| 01 | Veo, frames, 360p, 4 s | FAIL | Propeller motion works, but the face, blue eye ring, head banana and arm pose drift too far. |
| 02 | Veo, frames, 360p, 4 s | WARN / accepted motion base | Character, bucket and camera remain much more stable. Minor head-banana and face-detail drift remains; readable enough for the pilot. |
| 03 | Omni Flash, ingredients, custom Bongo voice, 360p, 4 s | WARN / rejected for final | Visually stable propeller take, but the prompt contained only “Bongo fixo.” and therefore omitted the required “OOOOOO… perfecto.” line. |
| 04 | Omni Flash, ingredients, custom Bongo voice, 360p, 4 s | PASS | Clear rotating banana propeller; Bongo, blue eye ring, single tooth, head banana, one blue left sandal, bucket, fan body, workshop and static camera remain stable. The exact prompt requests both scripted lines with a clear silent beat; the downloaded audio contains two separated voice regions with a 0.79 s pause. |

Verified Flow cost for each 360p / 4-second generation in this session: 4 credits. Total used: 32 credits.

## Final assembly

| Check | Result | Notes |
|---|---|---|
| Runtime | PASS | 12.000 s editorial timeline; MP4 container reports 12.022 s because of AAC frame padding. |
| Format | PASS | 360 × 640, 9:16, H.264, 24 fps, AAC stereo at 48 kHz. |
| Picture | PASS | No black frames; every cut lands on a valid image; final 0.5 s hold gives the catchphrase room to land. |
| Audio | PASS | Peak −1.1 dBFS; no clipping. Voice remains in front of three restrained bucket accents, a two-note original reveal sting and subtle filtered fan air. |
| Content | PASS | Problem, Bucketo, three Banga beats and banana-propeller payoff all read in sequence. |
| Listening | WARN | Automated checks confirm timing, separation and headroom, but a final human listening pass is still recommended before public upload. |

Final candidate: `output/pilot_001/pilot_001_final.mp4`

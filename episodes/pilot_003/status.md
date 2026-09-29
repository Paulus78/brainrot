# Pilot 003 — production status

## Current decision

`pilot_002_final_v1.mp4` remains a rejected motion proof. Pilot 003 is a full Veo motion rebuild, not another image-blend edit.

The story was simplified after the user's motion feedback and a review of current fruit/brainrot short-form patterns:

- Replace the tiny corn kernel with one absurdly huge normal corn cob that reads instantly on a phone.
- Remove the separate banana-drop scene.
- Replace three small taps with one large, physically staged double-palm slam.
- Preserve the banana-popcorn eruption and the dry `Bongo snacko.` button.
- Use three motion units so the final cut can flow without feeling like a slideshow.

## Current stage

- [x] New 3-shot story locked.
- [x] Initial frame-pair workflow tested and rejected because mismatched anchors forced an inconsistent scene.
- [x] Veo 3.1 Fast / 720p / image-element reference mode selected in Google Flow using Google Chrome.
- [x] Efficient retry policy locked: two variants in parallel, then at most one diagnosed retry.
- [x] Hook accepted after motion QC: reference-mode variant B.
- [x] Slam accepted after motion QC: reference-mode variant A.
- [x] Payoff accepted after motion QC: reference-mode variant B.
- [x] Consistent final voice and Veo foley mixed; only the accepted `Bongo snacko.` line is used.
- [x] 1080x1920 V1 master assembled and reviewed.

## Non-negotiable QC gates

1. The giant corn cob is present from the first frame and is visibly pushed/slurped completely into the bucket.
2. The slam contains anticipation, accelerating downstroke, simultaneous two-palm contact, bucket compression, body recoil and settle.
3. The payoff is a continuous eruption, not a dissolve between eruption stills.
4. Bongo retains the blue eye ring, banana peel, one front tooth and exactly one blue left sandal.
5. No shot is accepted only because its first or last frame looks good.
6. Generate two variants per scene first; a third attempt is allowed only for a diagnosed defect.

## Process correction

The first Pilot 003 Veo clip had usable motion, but its new start image was paired with an old end image from a different composition. Veo therefore had to reconcile two scenes. That attempt is rejected. From now on Bongo's original portrait is used only as an identity element; Veo is free to stage one coherent moving shot from the text prompt.

The corrected hook produced two coherent versions in one run. Variant B is selected because the huge corn cob remains readable, disappears fully into the bucket, and Bongo's involuntary hop gives the shot a stronger brainrot gag. Variant A remains a usable alternate.

The first two slam variants also produced real continuous motion. Variant A is selected because its bulging bucket, broad wind-up, strong squash and rebound create a much larger physical gag. Variant B is retained as the cleaner but less energetic alternate.

Payoff variant B is accepted on the first two-output run. Its warning pop, lean-in, expanding fountain, burial, re-emergence and bite form one readable continuous action. Variant A has a strong geyser but a confusing blue-sandal shape near the pile, so it remains only an alternate.

The completed V1 uses three long action units at a mild 1.08× pace and runs 19.96 seconds. It passes the silent cause-and-effect review and technical checks. Small independent-shot continuity differences remain documented in `qc/final_qc.md`, but the result is now a real moving brainrot short rather than a slideshow proof.

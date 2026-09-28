# Pilot 002 — voice master quality review

Updated: 2026-09-28 (Europe/Berlin)

## Goal

Create `Bucketo.` and `Bongo snacko.` in one uninterrupted generation so both lines retain the same speaker identity. The accepted voice must be warm, dry and slightly rough, without the high-register change heard in Pilot 001.

## Generation route

- Browser: Google Chrome.
- Workspace: the existing Bongo project in Google Flow.
- Model: Omni 1.1 Flash.
- Source frame: the existing `bongo.png` asset already stored in the Flow project.
- Format: one 8-second 9:16 take at 360p; the picture is only a carrier for the generated audio.
- Cost observed in Flow: 6 credits per take; two takes were generated for comparison.
- Flow scene URL: `https://flow.google.com/project/7c7f34d6-0a9f-4b16-a532-9abf6e5dc741/edit/3a15847b-eeaa-49f9-846d-f9220c12ae3b`

## Take 1 — accepted

The prompt locked both lines to one continuous take, one identical speaker, a warm mid-low creature register, slight nasal color and rasp, dry downward delivery, four seconds of silence between lines and no music or effects.

Source files:

- `audio/raw/voice_master_flow_omni_v1.mp4`
- `audio/raw/voice_master_flow_omni_v1.wav`
- accepted copy: `audio/accepted/voice_master_v1.wav`

Measured source performance:

| Check | `Bucketo.` | `Bongo snacko.` | Difference |
| --- | ---: | ---: | ---: |
| Speech region | 0.899–1.411 s | 5.469–6.315 s | 4.057 s clean gap |
| Median fundamental | 212.43 Hz | 224.35 Hz | +0.95 semitones |
| RMS level | -18.18 dBFS | -19.81 dBFS | -1.63 dB |

The full take contains only two near-full-scale peak samples and no flat-top clipping. The spectrogram shows the same harmonic spacing and broadly matching formant structure in both lines. The long gap is clean and contains no extra speech.

Decision: **PASS**. This take has no high-pitched identity jump and is suitable for the final mix.

## Take 2 — rejected

Take 2 added stronger instructions for lower, less regular and more conversational delivery.

Source files:

- `audio/raw/voice_master_flow_omni_v2.mp4`
- `audio/raw/voice_master_flow_omni_v2.wav`

Measured result:

| Check | `Bucketo.` | `Bongo snacko.` | Difference |
| --- | ---: | ---: | ---: |
| Median fundamental | 217.17 Hz | 275.34 Hz | +4.11 semitones |
| RMS level | -21.89 dBFS | -21.57 dBFS | +0.32 dB |

The second line rises much higher despite the prompt. A large unintended broadband sound also appears after roughly 7.19 seconds.

Decision: **REJECT**. The attempted naturalness correction reintroduced the exact pitch-identity problem and added unwanted sound.

## Final placement and level match

`src/edit/build_episode_002_final.sh` trims both accepted lines from Take 1, applies only short edge fades, gentle high/low filtering and static gain, and places them without time-stretching or pitch processing:

| Line | Audible final region | Visual beat |
| --- | ---: | --- |
| `Bucketo.` | 4.084–4.591 s | banana has fully disappeared; Bongo holds the confident gesture |
| `Bongo snacko.` | 11.915–12.763 s | eruption has settled; Bongo is visible with one snack |

The final voice-only check measures 217.60 Hz versus 226.12 Hz, a difference of only +0.67 semitones. The two line levels differ by 0.07 dB after the static level match. Final-program true peak is -1.1 dBFS.

Review artifacts:

- voice-only track: `output/pilot_002/pilot_002_voice_only_v1.wav`
- source spectrogram: `audio/voice_master_v1_spectrogram.png`
- dialogue placement stills: `audio/dialogue_placement_qc.png`

## Verdict

- One-session requirement: PASS.
- Exactly two separated voice regions: PASS.
- Pitch-identity check: PASS.
- Level consistency: PASS.
- No timing or pitch warping: PASS.
- Dialogue placement: PASS.
- Final human listening before public upload: still recommended, because numerical identity checks cannot fully judge charm or perceived naturalness.

# Prompting Guide – Bongo Bucket

## 1. Grundsatz

Prompts enthalten nur Informationen, die für den aktuellen Generationsschritt nötig sind.

## 2. Keyframe-Struktur

```text
[Character anchor]
[Pose]
[Props]
[Environment]
[Camera]
[Lighting/style]
[Constraints]
```

## 3. Shot-1-Beispiel

> Bongo Bucket, the established weird-cute monkey-like fantasy creature from the provided character reference: compact round tan-brown fuzzy body, oversized round ears, large slightly asymmetrical eyes, tiny nose, one oversized front tooth, small banana peel on top of his head. He stands beside his signature bright yellow plastic bucket with a simple black smiley face. In front of him on a small workbench is a simple desk fan that is clearly not spinning. Bongo looks at the fan with confused concern, head slightly tilted. Simple cozy cluttered garage/workshop background, only a few objects, no other characters. Vertical 9:16, medium shot, eye level, clear silhouette, warm stylized 3D cartoon lighting, clean readable shapes, weird-cute, not photorealistic, not gross.

## 4. Negative Guidance

> No additional characters, no clothing, no tongue hanging out, no saliva, no extra teeth, no realistic ape anatomy, no horror, no different bucket color, no living bucket face, no text labels, no complex background, no extra bananas unless requested.

## 5. Video-Prompt-Regel

Video-Prompt = Bewegung + Kamera + Stabilität.

Gut:
> Bongo stays in place and looks from the motionless fan to the yellow bucket. He tilts his head once. His ears make a small soft bounce. The fan remains completely still. Static eye-level camera. Preserve Bongo, bucket, fan and background appearance exactly.

## 6. Transformationen

Nicht zwingend live generieren.

Besser:
- vorher Keyframe A
- Cut
- Reveal-Keyframe B
- B leicht animieren

## 7. Pilot-Reveal

Keyframe:
> Same established Bongo and same workshop. The desk fan now has one absurd curved yellow banana functioning as its visible spinning propeller/blade assembly. The modification is clean, simple and immediately readable. Bongo stands beside it, proud and calm, yellow smiley bucket on the floor. No extra characters, no extra bananas. Vertical 9:16, medium shot.

Video:
> The banana propeller spins rapidly like a working fan. A strong but comedic stream of air pushes Bongo's oversized ears and soft fuzz backward slightly. Bongo remains planted and looks proud. The yellow bucket stays still. Static camera, no camera shake, no new objects, preserve character and prop design.

## 8. Komplexitätsalarm

Vereinfachen bei mehr als:
- 1 Character
- 2 wichtige Props
- 1 Hauptaktion
- 1 Kameraaktion
- 1 Transformation

## 9. Musik-Prompt

> Create a very short original absurd meme jingle around 110 BPM with toy-like percussion, a simple plucky mallet synth and tiny bass pulse. Catchy but minimal, slightly hypnotic, playful and strange rather than childish. Leave clear space for chant-like vocals. Include a brief stop before the reveal and a tiny sting for “perfecto”. Must loop cleanly and must not resemble any existing melody.

## 10. Versionierung

Jeder Prompt:
- ID
- Version
- created_at
- provider
- model
- purpose
- episode/shot

Erfolgreiche Prompts nie still überschreiben.

# Bongo 1% (ep004) - Code-Animations-Experiment

Komplett deterministisch gerendert (Python: OpenCV/NumPy/PIL + ffmpeg), kein Veo.

- Render:  `python src/anim/render.py --tag v03`   (Frames parallel, ~75 s)
- Audio:   `python src/anim/voice.py --preset A` (Stimme), `python src/anim/mix.py <out.wav>` (SFX+Mix)
- Preview: `python src/anim/preview.py out.png 0.5 1.2 ...` (einzelne Zeitpunkte als Kontaktbogen)
- Rig:     `python src/anim/cutout.py && python src/anim/build_rig.py` (Layer aus `assets/character_master/bongo_reference.png`)
- Zeitplan: `src/anim/timeline.py`, Choreografie: `src/anim/story.py`

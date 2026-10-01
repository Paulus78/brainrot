"""Lokale Spracherkennung (faster-whisper): prueft, ob Bongos Zeilen verstaendlich sind, und liefert Wort-Zeiten.
Aufruf: python src/flowrig/asr.py clip1.mp4 clip2.mp4 ..."""
import sys, subprocess, numpy as np, json, warnings
warnings.filterwarnings('ignore')
from faster_whisper import WhisperModel

def audio(path):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', path, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768

def words(path, model=None):
    model = model or WhisperModel('small.en', device='cpu', compute_type='int8')
    segs, _ = model.transcribe(audio(path), word_timestamps=True, vad_filter=False, initial_prompt='Bongo. Bongo food. Bongo bucketo. Bongo fixo. Bongo banana. Bongo no.')
    return [(w.word.strip(), round(w.start, 2), round(w.end, 2)) for s in segs for w in s.words]

if __name__ == '__main__':
    m = WhisperModel('small.en', device='cpu', compute_type='int8')
    for p in sys.argv[1:]:
        print(p.split('/')[-1], json.dumps(words(p, m)))

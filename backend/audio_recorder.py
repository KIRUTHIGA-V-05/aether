import sounddevice as sd
import numpy as np
import librosa
import soundfile as sf

def record_and_save(filename="command.wav", duration=3, fs=16000):
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    sf.write(filename, recording, fs)
    return filename

def preprocess_audio(filename):
    y, sr = librosa.load(filename, sr=16000)
    y_trimmed, _ = librosa.effects.trim(y)
    sf.write(filename, y_trimmed, sr)

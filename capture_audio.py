import sounddevice as sd
import soundfile as sf


def record_wav(path: str, seconds: float = 10.0, sr: int = 16000):
    audio = sd.rec(int(seconds * sr), samplerate=sr, channels=1, dtype="float32")
    sd.wait()
    sf.write(path, audio, sr)
    return path


if __name__ == "__main__":
    record_wav("test.wav", seconds=5)
    print("saved test.wav")

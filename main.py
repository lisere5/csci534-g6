import time
from capture_audio import record_wav
from features_audio import transcribe, audio_confusion_features
from features_eye import capture_eye_features
from confusion import confusion_score, is_confused

LESSON = [
    "Segment 1: The event begins with ...",
    "Segment 2: A key turning point was ...",
    "Segment 3: The outcome was influenced by ...",
]

def adapt_text(original: str):
    # Replace later with an LLM call if you want
    return "Let me re-explain more simply: " + original

def run():
    for i, seg in enumerate(LESSON, start=1):
        print("\n" + "="*60)
        print(f"TEACHING {i}: {seg}")
        print("Now, explain back what you understood (10 seconds).")

        # Record simultaneously: easiest MVP is sequential capture windows.
        # For better sync, run audio+video in parallel threads later.
        eye = capture_eye_features(seconds=10)
        wav_path = record_wav(f"data/sessions/resp_{i}.wav", seconds=10)

        wres = transcribe(wav_path)
        aud = audio_confusion_features(wres)

        score = confusion_score(aud, eye)

        print("\n--- Features ---")
        print("Transcript:", aud["transcript"])
        print("Audio feats:", {k: aud[k] for k in ["word_count","filler_count","long_pause_count","wpm"]})
        print("Eye feats:", eye)
        print("Confusion score:", round(score, 3))

        if is_confused(score):
            print("\n[ADAPT] Confusion detected. Adjusting explanation...")
            print(adapt_text(seg))
        else:
            print("\n[OK] Continuing...")

if __name__ == "__main__":
    run()
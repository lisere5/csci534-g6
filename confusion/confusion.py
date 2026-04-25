import string


def confusion_score(audio_feats: dict, eye_feats: dict):
    score = 0.0

    filler = audio_feats.get("filler_count", 0)
    long_pauses = audio_feats.get("long_pause_count", 0)
    wpm = audio_feats.get("wpm", 0.0)
    low_response = audio_feats.get("low_response", False)
    transcript = audio_feats.get("transcript", "")

    blink_rate = eye_feats.get("blink_rate", 0.0)
    face_missing = eye_feats.get("face_missing_ratio", 0.0)

    if transcript:
        words = transcript.split()
        # normalize: lowercase + remove punctuation
        cleaned_words = [
            w.lower().strip(string.punctuation) for w in words
        ]
        print(f"Transcript words: {cleaned_words}")

        if cleaned_words.count("no") > 0 or cleaned_words.count("don't") > 0:
            print("Detected multiple negative words in transcript")
            score += 2.0

    if filler >= 3:
        score += 2.0
        print(f"Detected {filler} filler words, which may indicate confusion.")

    if long_pauses >= 2:
        score += 2.0
        print(f"Detected {long_pauses} long pauses, which may indicate confusion.")

    if low_response:
        score += 2.0
        print(f"Detected low response level, which may indicate confusion.")

    if wpm > 0 and wpm < 90:
        score += 1.0
        print(f"Detected low speaking rate of {wpm:.1f} WPM, which may indicate confusion.")

    if blink_rate > 0.6:
        score += 1.0
        print(f"Detected high blink rate of {blink_rate:.2f} blinks/sec, which may indicate confusion.")

    if face_missing >= 0.20:
        score += 2.0
        print(f"Detected face missing ratio of {face_missing:.2f}, which may indicate confusion or disengagement.")

    return score


def is_confused(score: float, threshold: float = 3.0):
    return score >= threshold

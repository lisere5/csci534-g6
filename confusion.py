def confusion_score(audio_feats: dict, eye_feats: dict):
    score = 0.0

    filler = audio_feats.get("filler_count", 0)
    long_pauses = audio_feats.get("long_pause_count", 0)
    wpm = audio_feats.get("wpm", 0.0)
    low_response = audio_feats.get("low_response", False)

    blink_rate = eye_feats.get("blink_rate", 0.0)
    face_missing = eye_feats.get("face_missing_ratio", 0.0)

    if filler >= 3:
        score += 2.0

    if long_pauses >= 2:
        score += 2.0

    if low_response:
        score += 2.0

    if wpm > 0 and wpm < 90:
        score += 1.0

    if blink_rate > 0.6:
        score += 1.0

    if face_missing >= 0.20:
        score += 2.0

    return score


def is_confused(score: float, threshold: float = 3.0):
    return score >= threshold

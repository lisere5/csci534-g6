def confusion_score(audio_feats: dict, eye_feats: dict):
    # Normalize-ish using simple heuristics (tune after pilot)
    filler = audio_feats["filler_count"]
    long_pauses = audio_feats["long_pause_count"]
    wpm = audio_feats["wpm"]

    blink_rate = eye_feats["blink_rate"]
    face_missing = eye_feats["face_missing_ratio"]

    score = 0.0
    score += 0.6 * min(filler / 3.0, 1.0)
    score += 0.8 * min(long_pauses / 2.0, 1.0)

    # Very low speaking rate can mean struggle/hesitation (careful!)
    if wpm > 0:
        score += 0.6 * min(max(0.0, (120.0 - wpm) / 120.0), 1.0)

    # More blinking + looking away can be load/disengagement
    score += 0.5 * min(blink_rate / 0.6, 1.0)      # ~0.2–0.6 blinks/sec common-ish
    score += 1.0 * min(face_missing / 0.25, 1.0)   # lots of face-missing = likely looking away

    return score

def is_confused(score: float, threshold: float = 1.5):
    return score >= threshold
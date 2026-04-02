import whisper
import re

_model = None

def transcribe(path: str):
    global _model
    if _model is None:
        _model = whisper.load_model("base")  # tiny/base/small
    result = _model.transcribe(path, fp16=False)
    return result  # contains text + segments + timestamps

FILLERS = {"um", "uh", "erm", "like", "you know"}

def audio_confusion_features(whisper_result: dict):
    text = (whisper_result.get("text") or "").lower()
    words = re.findall(r"[a-z']+", text)

    filler_count = sum(1 for w in words if w in FILLERS)
    word_count = len(words)

    # pause proxy: count "gaps" between whisper segments
    segs = whisper_result.get("segments") or []
    gaps = []
    for i in range(1, len(segs)):
        gaps.append(max(0.0, segs[i]["start"] - segs[i-1]["end"]))
    long_pause_count = sum(1 for g in gaps if g > 0.8)

    duration = 0.0
    if segs:
        duration = segs[-1]["end"] - segs[0]["start"]

    wpm = (word_count / max(duration, 1e-6)) * 60.0 if duration > 0 else 0.0

    return {
        "word_count": word_count,
        "filler_count": filler_count,
        "long_pause_count": long_pause_count,
        "wpm": wpm,
        "transcript": whisper_result.get("text", "").strip()
    }
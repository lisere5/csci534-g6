import cv2
import mediapipe as mp
import numpy as np
from collections import deque

mp_face = mp.solutions.face_mesh

# Simple Eye Aspect Ratio (EAR) using 6 landmarks per eye.
# FaceMesh landmark indices:
# Right eye: 33, 160, 158, 133, 153, 144
# Left eye: 362, 385, 387, 263, 373, 380
RIGHT = [33, 160, 158, 133, 153, 144]
LEFT  = [362, 385, 387, 263, 373, 380]

def _ear(pts):
    # pts: 6x2
    A = np.linalg.norm(pts[1] - pts[5])
    B = np.linalg.norm(pts[2] - pts[4])
    C = np.linalg.norm(pts[0] - pts[3])
    return (A + B) / (2.0 * C + 1e-6)

def capture_eye_features(seconds=10.0, cam_index=0, ear_thresh=0.21):
    cap = cv2.VideoCapture(cam_index)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if not fps or fps < 5:
        fps = 30.0

    total_frames = int(seconds * fps)
    face_missing = 0

    blinks = 0
    was_closed = False

    with mp_face.FaceMesh(
        static_image_mode=False,
        refine_landmarks=True,
        max_num_faces=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as mesh:

        for _ in range(total_frames):
            ok, frame = cap.read()
            if not ok:
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            res = mesh.process(rgb)

            if not res.multi_face_landmarks:
                face_missing += 1
                was_closed = False
                continue

            lm = res.multi_face_landmarks[0].landmark
            h, w = frame.shape[:2]

            def to_xy(i):
                return np.array([lm[i].x * w, lm[i].y * h], dtype=np.float32)

            r = np.vstack([to_xy(i) for i in RIGHT])
            l = np.vstack([to_xy(i) for i in LEFT])
            ear = (_ear(r) + _ear(l)) / 2.0

            closed = ear < ear_thresh

            # blink count: closed → open transition
            if was_closed and not closed:
                blinks += 1
            was_closed = closed

    cap.release()

    face_missing_ratio = face_missing / max(total_frames, 1)
    blink_rate = blinks / max(seconds, 1e-6)  # blinks per second

    return {
        "blinks": blinks,
        "blink_rate": blink_rate,
        "face_missing_ratio": face_missing_ratio
    }

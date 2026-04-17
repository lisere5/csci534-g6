from confusion.features_eye import capture_eye_features


def record_video_features(seconds: float = 10.0, cam_index: int = 0):
    return capture_eye_features(seconds=seconds, cam_index=cam_index)


if __name__ == "__main__":
    feats = record_video_features(seconds=5)
    print("Video/Eye features:", feats)

import os
import cv2

VIDEO_DIR = "data/key_videos"
VIDEO_EXTS = (".mp4", ".avi", ".mov", ".mkv")

def check_videos(video_dir=VIDEO_DIR):
    """
    Attempts to open each video file in `video_dir` and read one frame.
    Returns a dict: { filename: True (ok) / False (fail) }.
    """
    results = {}
    for fname in sorted(os.listdir(video_dir)):
        if not fname.lower().endswith(VIDEO_EXTS):
            continue

        path = os.path.join(video_dir, fname)
        cap = cv2.VideoCapture(path)
        if not cap.isOpened():
            results[fname] = False
            print(f"[ERROR] Cannot open {fname}")
            continue

        ret, frame = cap.read()
        if not ret or frame is None:
            results[fname] = False
            print(f"[ERROR] Cannot read frame from {fname}")
        else:
            results[fname] = True
            print(f"[ OK ] {fname} plays correctly")

        cap.release()

    return results

if __name__ == "__main__":
    summary = check_videos()
    total = len(summary)
    ok = sum(1 for v in summary.values() if v)
    fail = total - ok

    print("\n=== Summary ===")
    print(f"Total videos checked: {total}")
    print(f"Playable: {ok}")
    print(f"Failures: {fail}")
    if fail:
        print("Failed files:")
        for fname, passed in summary.items():
            if not passed:
                print("  -", fname)

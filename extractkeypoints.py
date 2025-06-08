import cv2
import mediapipe as mp
import os
import json
import logging
from tqdm import tqdm

# Initialize logging
logging.basicConfig(filename="keypoint_extraction.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize Mediapipe holistic model
mp_holistic = mp.solutions.holistic  
mp_drawing = mp.solutions.drawing_utils

# Paths
VIDEO_DIR = "data/video"  
KEYPOINT_DIR = "data/key"  
os.makedirs(KEYPOINT_DIR, exist_ok=True)

# Frame processing interval (every Nth frame)
FRAME_SKIP = 2  

def extract_keypoints(video_path):
    """Extracts keypoints (pose, hands, face) from a video."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        logging.error(f"Could not open video: {video_path}")
        return None

    keypoints_list = []
    frame_count = 0

    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break  

            # Process every Nth frame
            frame_count += 1
            if frame_count % FRAME_SKIP != 0:
                continue  

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = holistic.process(frame_rgb)  

            keypoints = {
                "pose": [[lm.x, lm.y, lm.z] for lm in results.pose_landmarks.landmark] if results.pose_landmarks else [],
                "left_hand": [[lm.x, lm.y, lm.z] for lm in results.left_hand_landmarks.landmark] if results.left_hand_landmarks else [],
                "right_hand": [[lm.x, lm.y, lm.z] for lm in results.right_hand_landmarks.landmark] if results.right_hand_landmarks else [],
                "face": [[lm.x, lm.y, lm.z] for lm in results.face_landmarks.landmark] if results.face_landmarks else []
            }

            keypoints_list.append(keypoints)

    cap.release()
    return keypoints_list

def process_all_videos():
    """Processes all videos and extracts keypoints as JSON."""
    for video_file in tqdm(os.listdir(VIDEO_DIR), desc="Processing Videos"):
        if video_file.endswith(".mp4"):
            video_path = os.path.join(VIDEO_DIR, video_file)
            gesture_name = os.path.splitext(video_file)[0]  

            keypoints = extract_keypoints(video_path)
            if keypoints:
                json_path = os.path.join(KEYPOINT_DIR, f"{gesture_name}.json")
                with open(json_path, "w") as f:
                    json.dump(keypoints, f, indent=4)
                logging.info(f"Saved keypoints: {json_path}")
            else:
                logging.warning(f"Skipped: {video_file}")

    logging.info("Keypoint extraction completed!")

if __name__ == "__main__":
    process_all_videos()

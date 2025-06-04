import os
import json
import time
import psutil
from collections import defaultdict
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from sentence_transformers import SentenceTransformer, util

# One-time NLTK downloads
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

# Configuration (same as your Flask app)
KEYPOINT_DIR = "data/key"
HUMAN_VIDEO_DIR = "data/video"
STOPWORDS = set(stopwords.words("english")) - {"who", "what", "where", "when", "why", "how"}

# Load BERT model
bert_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Reuse your preprocessing functions
def preprocess_text(text):
    return [w for w in word_tokenize(text.lower()) if w not in STOPWORDS]

def expand_query_with_synonyms(word):
    syns = set()
    for s in wordnet.synsets(word):
        for lem in s.lemmas():
            syns.add(lem.name())
    return syns

def calculate_similarity(user_input, candidate):
    candidate_text = candidate.replace("_", " ")
    user_embedding = bert_model.encode(user_input, convert_to_tensor=True)
    candidate_embedding = bert_model.encode(candidate_text, convert_to_tensor=True)
    similarity = util.cos_sim(user_embedding, candidate_embedding)
    return float(similarity.cpu().numpy())

def find_matching_keypoints(user_input):
    files = {
        fname[:-5]: os.path.join(KEYPOINT_DIR, fname)
        for fname in os.listdir(KEYPOINT_DIR) if fname.endswith(".json")
    }
    candidates = set()
    phrase = user_input.replace(" ", "_")
    if phrase in files:
        candidates.add(phrase)
    for w in preprocess_text(user_input):
        if w in files:
            candidates.add(w)
        else:
            for syn in expand_query_with_synonyms(w):
                if syn in files:
                    candidates.add(syn)
                    break
    results = []
    for candidate in candidates:
        score = calculate_similarity(user_input, candidate)
        results.append((candidate, score))
    results.sort(key=lambda x: x[1], reverse=True)
    return results

# Mock test dataset (replace with your actual dataset)
TEST_DATASET = [
    ("hello world", ["hello", "world"]),
    ("good morning", ["good_morning"]),
    ("thank you", ["thank_you"]),
    ("how are you", ["how_are_you"]),
    ("sign language", ["sign_language"]),
    # Add more test cases as needed
] * 10  # Repeat to simulate 50 queries

# Mock file existence (replace with actual file checks)
MOCK_KEYPOINTS = {"hello", "world", "good_morning", "thank_you", "how_are_you", "sign_language"}
MOCK_VIDEOS = {"hello.mp4", "world.mp4", "thank_you.mp4", "sign_language.mp4"}

def evaluate_metrics():
    metrics = {}
    process = psutil.Process(os.getpid())
    
    # Initialize counters
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    similarity_scores_correct = []
    similarity_scores_incorrect = []
    video_retrieval_success = 0
    video_retrieval_total = 0
    input_handling_correct = 0
    input_handling_total = 0
    response_times = []
    
    # Test each input
    for user_input, expected_keypoints in TEST_DATASET:
        input_handling_total += 1
        start_time = time.time()
        
        # Handle empty/invalid input
        if not user_input.strip():
            input_handling_correct += 1  # Correctly flagged empty input
            continue
        
        # Process valid input
        try:
            keyword_results = find_matching_keypoints(user_input)
            input_handling_correct += 1
        except Exception:
            continue
        
        # Evaluate keypoint matching
        retrieved_keypoints = {kp for kp, _ in keyword_results}
        expected_set = set(expected_keypoints)
        correct_matches = retrieved_keypoints.intersection(expected_set)
        
        true_positives += len(correct_matches)
        false_positives += len(retrieved_keypoints - expected_set)
        false_negatives += len(expected_set - retrieved_keypoints)
        
        # Collect similarity scores
        for kp, score in keyword_results:
            if kp in expected_set:
                similarity_scores_correct.append(score)
            else:
                similarity_scores_incorrect.append(score)
        
        # Evaluate video retrieval
        for kp, _ in keyword_results:
            fname = f"{kp}.mp4"
            video_retrieval_total += 1
            if fname in MOCK_VIDEOS:  # Replace with os.path.exists(os.path.join(HUMAN_VIDEO_DIR, fname))
                video_retrieval_success += 1
        
        # Measure response time
        response_times.append(time.time() - start_time)
    
    # Compute metrics
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    avg_similarity_correct = np.mean(similarity_scores_correct) if similarity_scores_correct else 0
    avg_similarity_incorrect = np.mean(similarity_scores_incorrect) if similarity_scores_incorrect else 0
    video_retrieval_rate = video_retrieval_success / video_retrieval_total if video_retrieval_total > 0 else 0
    input_handling_accuracy = input_handling_correct / input_handling_total if input_handling_total > 0 else 0
    avg_response_time = np.mean(response_times) if response_times else 0
    memory_usage_mb = process.memory_info().rss / (1024 * 1024)  # Convert bytes to MB
    
    # Store metrics
    metrics["precision"] = round(precision, 3)
    metrics["recall"] = round(recall, 3)
    metrics["f1_score"] = round(f1_score, 3)
    metrics["avg_similarity_correct"] = round(avg_similarity_correct, 3)
    metrics["avg_similarity_incorrect"] = round(avg_similarity_incorrect, 3)
    metrics["video_retrieval_rate"] = round(video_retrieval_rate, 3)
    metrics["input_handling_accuracy"] = round(input_handling_accuracy, 3)
    metrics["avg_response_time_seconds"] = round(avg_response_time, 3)
    metrics["memory_usage_mb"] = round(memory_usage_mb, 2)
    
    # Save to JSON
    with open("evaluation_metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)
    
    return metrics

if __name__ == "__main__":
    print("Evaluating metrics...")
    results = evaluate_metrics()
    print("\nEvaluation Metrics:")
    for metric, value in results.items():
        print(f"{metric.replace('_', ' ').title()}: {value}")
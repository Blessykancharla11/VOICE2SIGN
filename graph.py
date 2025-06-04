import matplotlib.pyplot as plt
import numpy as np

# Evaluation metrics
metrics = {
    "precision": 0.444,
    "recall": 0.667,
    "f1_score": 0.533,
    "input_handling_accuracy": 1.0,
    "avg_similarity_correct": 0.938,
    "avg_similarity_incorrect": 0.479,
    "video_retrieval_rate": 0.222,
    "avg_response_time_seconds": 0.109,
    "memory_usage_mb": 376.2
}

# Plot 1: Accuracy Metrics
fig, ax = plt.subplots(figsize=(8, 4))
labels = ["Precision", "Recall", "F1-Score", "Input Handling"]
values = [metrics["precision"], metrics["recall"], metrics["f1_score"], metrics["input_handling_accuracy"]]
colors = ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2"]
ax.bar(labels, values, color=colors)
ax.set_ylim(0, 1)
ax.set_ylabel("Score")
ax.set_title("Accuracy Metrics for Voice2Sign System")
for i, v in enumerate(values):
    ax.text(i, v + 0.02, f"{v:.3f}", ha="center")
plt.tight_layout()
plt.savefig("accuracy_metrics.png", dpi=300)
plt.close()

# Plot 2: Cosine Similarity Scores
fig, ax = plt.subplots(figsize=(6, 4))
labels = ["Correct Matches", "Incorrect Matches"]
values = [metrics["avg_similarity_correct"], metrics["avg_similarity_incorrect"]]
colors = ["#59a14f", "#edc949"]
ax.bar(labels, values, color=colors)
ax.set_ylim(0, 1)
ax.set_ylabel("Cosine Similarity Score")
ax.set_title("Cosine Similarity Scores for Voice2Sign System")
for i, v in enumerate(values):
    ax.text(i, v + 0.02, f"{v:.3f}", ha="center")
plt.tight_layout()
plt.savefig("similarity_scores.png", dpi=300)
plt.close()

# Plot 3: System Efficiency Metrics
fig, ax = plt.subplots(figsize=(8, 4))
labels = ["Video Retrieval Rate", "Response Time (s)", "Memory Usage (MB)"]
values = [metrics["video_retrieval_rate"], metrics["avg_response_time_seconds"], metrics["memory_usage_mb"]]
colors = ["#bc5090", "#ff6361", "#003f5c"]
ax.bar(labels, values, color=colors)
ax.set_ylabel("Value")
ax.set_title("System Efficiency Metrics for Voice2Sign System")
for i, v in enumerate(values):
    ax.text(i, v + max(values)*0.02, f"{v:.3f}", ha="center")
plt.tight_layout()
plt.savefig("efficiency_metrics.png", dpi=300)
plt.close()

print("Graphs saved as: accuracy_metrics.png, similarity_scores.png, efficiency_metrics.png")
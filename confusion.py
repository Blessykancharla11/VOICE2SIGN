import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

# Mock test dataset and predictions (replace with your actual data)
# Simulated based on 50 inputs, low precision (0.444), high incorrect similarity (0.479)
classes = ["hello", "world", "good_morning", "thank_you", "how_are_you"]
true_labels = [
    "hello", "hello", "world", "world", "good_morning", "good_morning", 
    "thank_you", "thank_you", "how_are_you", "how_are_you"
] * 5  # 50 inputs
# Simulated predictions with errors (e.g., "hello" misclassified as "hi" or "world")
predicted_labels = [
    "hello", "world", "world", "hello", "good_morning", "thank_you", 
    "thank_you", "how_are_you", "how_are_you", "good_morning"
] * 5  # Mimics low precision

# Compute confusion matrix
cm = confusion_matrix(true_labels, predicted_labels, labels=classes)
cm_normalized = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]  # Normalize for percentages

# Plot confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(
    cm_normalized, 
    annot=True, 
    fmt=".2f", 
    cmap="Blues", 
    xticklabels=classes, 
    yticklabels=classes,
    cbar_kws={"label": "Normalized Count"}
)
plt.title("Normalized Confusion Matrix for Voice2Sign System")
plt.xlabel("Predicted Keypoint")
plt.ylabel("True Keypoint")
plt.xticks(rotation=45, ha="right")
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig("confusion_matrix.png", dpi=300)
plt.close()

print("Confusion matrix saved as: confusion_matrix.png")
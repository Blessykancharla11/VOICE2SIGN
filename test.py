#!/usr/bin/env python3
import sys
import pandas as pd

# Import your matching function
from app import find_matching_keypoints

def test_gestures(gestures_csv: str, output_csv: str):
    # Load the CSV of test cases
    df = pd.read_csv(gestures_csv)

    records = []
    for _, row in df.iterrows():
        # Normalize the ground-truth name and prepare user input
        name = str(row['name']).strip()
        user_input = name.replace('_', ' ').lower()

        # Call your function
        matches = find_matching_keypoints(user_input)
        if matches:
            predicted, score = matches[0]
            predicted_norm = predicted.lower()
        else:
            predicted_norm, score = None, 0.0

        # Compare lowercase-to-lowercase
        correct = (predicted_norm == name.lower())

        records.append({
            'name':             name,
            'input':            user_input,
            'expected':         name,
            'predicted':        predicted,
            'similarity_score': score,
            'correct':          correct
        })

    # Save the results
    results_df = pd.DataFrame(records)
    results_df.to_csv(output_csv, index=False)

    # Print overall Top-1 accuracy
    acc = results_df['correct'].mean()
    print(f"Top-1 accuracy: {acc*100:.2f}% over {len(results_df)} samples")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python test.py <gestures.csv> <results.csv>")
        sys.exit(1)

    gestures_csv = sys.argv[1]
    output_csv   = sys.argv[2]
    test_gestures(gestures_csv, output_csv)

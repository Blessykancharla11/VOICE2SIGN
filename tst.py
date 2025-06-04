#!/usr/bin/env python3
import csv
import os
import sys

# Import your matching function
from app import find_matching_keypoints

def main():
    print("Interactive Gesture Tester")
    print("Enter gesture names one per line. When finished, just press ENTER on an empty line.\n")

    gestures = []
    while True:
        name = input("Gesture name (use underscores for spaces, e.g. Thank_You): ").strip()
        if not name:
            break
        gestures.append(name)

    if not gestures:
        print("No gestures entered. Exiting.")
        sys.exit(0)

    # Ask for output file
    default_out = "interactive_results.csv"
    out_path = input(f"\nOutput CSV file [{default_out}]: ").strip() or default_out

    # Run matching for each
    records = []
    for name in gestures:
        user_input = name.replace('_', ' ').lower()
        matches = find_matching_keypoints(user_input)
        if matches:
            predicted, score = matches[0]
        else:
            predicted, score = None, 0.0
        correct = (predicted is not None) and (predicted.lower() == name.lower())

        records.append({
            'name':             name,
            'input':            user_input,
            'predicted':        predicted,
            'similarity_score': score,
            'correct':          correct
        })

    # Write CSV
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['name','input','predicted','similarity_score','correct'])
        writer.writeheader()
        writer.writerows(records)

    print(f"\nResults written to {os.path.abspath(out_path)}")
    # Print a quick summary
    total = len(records)
    correct_count = sum(1 for r in records if r['correct'])
    print(f"Top-1 accuracy on your inputs: {correct_count}/{total} = {correct_count/total*100:.2f}%")

if __name__ == "__main__":
    main()

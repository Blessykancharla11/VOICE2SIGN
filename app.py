import os
from flask import Flask, render_template, request, flash, send_from_directory
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
import numpy as np
from sentence_transformers import SentenceTransformer, util

# One‑time NLTK downloads
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

# Configuration
KEYPOINT_DIR    = "data/key"
HUMAN_VIDEO_DIR = "data/video"
STOPWORDS       = set(stopwords.words("english")) - {"who", "what", "where", "when", "why", "how"}

# Load the BERT model
bert_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def preprocess_text(text):
    return [w for w in word_tokenize(text.lower()) if w not in STOPWORDS]

def expand_query_with_synonyms(word):
    syns = set()
    for s in wordnet.synsets(word):
        for lem in s.lemmas():
            syns.add(lem.name())
    return syns

def calculate_similarity(user_input, candidate):
    """
    Compute the cosine similarity between the user's input and the candidate keypoint phrase.
    The candidate phrase is assumed to be a string (with underscores removed for readability).
    """
    # Normalize candidate phrase: replace underscores with spaces
    candidate_text = candidate.replace("_", " ")
    user_embedding = bert_model.encode(user_input, convert_to_tensor=True)
    candidate_embedding = bert_model.encode(candidate_text, convert_to_tensor=True)
    similarity = util.cos_sim(user_embedding, candidate_embedding)  # returns a tensor
    return float(similarity.cpu().numpy())

def find_matching_keypoints(user_input):
    # Map keypoint base names to file paths
    files = {
        fname[:-5]: os.path.join(KEYPOINT_DIR, fname)
        for fname in os.listdir(KEYPOINT_DIR) if fname.endswith(".json")
    }
    candidates = set()
    # 1) full‑phrase match (replace spaces with underscores)
    phrase = user_input.replace(" ", "_")
    if phrase in files:
        candidates.add(phrase)
    # 2) word‑by‑word matching and synonym expansion
    for w in preprocess_text(user_input):
        if w in files:
            candidates.add(w)
        else:
            for syn in expand_query_with_synonyms(w):
                if syn in files:
                    candidates.add(syn)
                    break

    # For each candidate, calculate the similarity score with the full user_input
    results = []
    for candidate in candidates:
        score = calculate_similarity(user_input, candidate)
        results.append((candidate, score))
    # Sort results by score in descending order (more similar first)
    results.sort(key=lambda x: x[1], reverse=True)
    return results

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Home route: initial landing page
@app.route('/')
def home():
    return render_template('home.html')

# Converter route: shows the main converter functionality
@app.route('/converter', methods=["GET", "POST"])
def converter():
    user_input  = None
    keyword_results = []  # will hold tuples (keypoint, similarity_score)
    video_files = []
    input_type  = request.form.get("input_type", "text")

    if request.method == "POST":
        # Read text or voice input
        if input_type == "voice":
            user_input = request.form.get("voice_input", "").strip().lower()
        else:
            user_input = request.form.get("user_input", "").strip().lower()

        if not user_input:
            flash("Please enter some text or use the mic.")
        else:
            # Find matching keypoints along with their similarity scores
            keyword_results = find_matching_keypoints(user_input)
            if not keyword_results:
                flash("No matching keypoints found.")
            else:
                # Build list of existing video files for keypoints
                for kp, score in keyword_results:
                    fname = f"{kp}.mp4"
                    path  = os.path.join(HUMAN_VIDEO_DIR, fname)
                    if os.path.exists(path):
                        video_files.append(fname)
                    else:
                        flash(f"Video not found for keypoint: {kp}")

    return render_template(
        "index.html",
        input_type=input_type,
        user_input=user_input,
        keyword_results=keyword_results,  # Pass list of (keypoint, score) tuples to the template
        video_files=video_files
    )

# Route to serve video files
@app.route("/video/<filename>")
def serve_video(filename):
    return send_from_directory(HUMAN_VIDEO_DIR, filename)

# About page route
@app.route('/about')
def about():
    return render_template('about.html')

# Contact page route
@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True, port=5001)

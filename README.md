# VOICE2SIGN : Enabling Communication Through Gestures 🔈🤟

**VOICE2SIGN** VOICE2SIGN is an innovative assistive technology application designed to translate spoken or written language into Indian Sign Language (ISL) gestures. By leveraging advanced machine learning techniques such as pose keypoint extraction and speech recognition, VOICE2SIGN bridges communication gaps for the deaf and hard-of-hearing community. The system processes YouTube gesture videos, extracts meaningful sign language keypoints, and offers real-time translation through an intuitive web interface, empowering users to communicate more effectively and inclusively.


---

<img src="https://github.com/user-attachments/assets/d740dcf9-e6bc-4c7f-92f5-c6757169104c" alt="Speech Recognition" width="400"/>


## 💡 Features

- 🎙️ **Real-time Speech-to-Sign** translation  
- ⌨️ **Instant Text-to-Sign** translation  
- 🧠 **Keypoint Extraction** using MediaPipe  
- 📹 Support for custom ISL gesture videos  
- 🌐 Simple, responsive web interface  

---

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS, JavaScript  
- **Backend**: Python (Flask)  
- **Media & ML**: OpenCV, MediaPipe  
- **Speech Recognition**: SpeechRecognition Python library  
- **Video Source**: YouTube + CSV-based trimming  

---

##  Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Blessykancharla11/VOICE2SIGN.git
cd VOICE2SIGN
```
---

### 📦 2. Install Dependencies

Make sure you have Python installed, then run:

```bash
pip install -r requirements.txt
```

---

### 📹 3. Download & Trim Gesture Videos

This script downloads ISL gesture videos and trims them based on the entries in the `videos.csv` file:

```bash
python download.py
```

---

### 🧠 4. Extract Keypoints using MediaPipe

This step processes each trimmed video and extracts keypoints, which are saved in the `data/keypoints/` directory:

```bash
python extractkeypoints.py
```

---

### 🚀 5. Launch the Web App

Start the Flask server by running:

```bash
python app.py
```

Then open your browser and go to:

[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

### Screenshots

<img width="600" alt="Screenshot 2025-06-05 at 1 07 55 PM" src="https://github.com/user-attachments/assets/e2ec8d70-499d-4fa5-b06a-442899be82ed" />


<img width="600" alt="s2" src="https://github.com/user-attachments/assets/33c9ac26-9126-49e1-8958-c2f128dd7d99" />


<img width="600" alt="s3" src="https://github.com/user-attachments/assets/017ccc0a-1289-424a-aa20-daf29449cac4" />


---

## Conclusion

VOICE2SIGN demonstrates a practical and impactful approach to bridging communication barriers between hearing and non-hearing individuals through technology. By combining speech recognition, video processing, and machine learning-based keypoint extraction, the project provides an accessible platform for translating spoken and written language into Indian Sign Language gestures. This work not only highlights the potential of AI in assistive technologies but also contributes towards fostering greater inclusivity and understanding within the community. Future enhancements could include expanding gesture datasets, improving real-time accuracy, and integrating more languages to broaden its usability.

---

## Copyright
© 2025 Voice2Sign. All rights reserved.


With love❤️ BlessyKancharla11

Thank you for exploring VOICE2SIGN!
Feel free to reach out for collaboration, feedback, or support.
Let’s build a more inclusive world together!




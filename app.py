from flask import Flask, request, jsonify
import cv2
import numpy as np
from keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
emotion_classifier = load_model('model.h5')

emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
cap = cv2.VideoCapture(0)
start_time = time.time()
first_chat_after_hey = True  # Flag to track the first chat after 'hey'
detected_emotion = None  # Detected emotion placeholder

@app.route('/chat', methods=['POST'])
def chat():
    message = request.json['message']

    # Check if the user's message is 'hey'
    if message.lower() == 'hey':
        response = handle_hey()
    else:
        response = handle_chat(message)

    print(f'Response: {response}')
    return jsonify({'message': response})

def handle_hey():
    global first_chat_after_hey, detected_emotion
    first_chat_after_hey = True  # Reset the flag for the first chat after 'hey'
    detected_emotion = None  # Reset the detected emotion
    return "Hello, I am SerenityNow."

def handle_chat(message):
    global first_chat_after_hey, detected_emotion
    response = ""
    if first_chat_after_hey:
        if detected_emotion:
            response = f"I sense that you're feeling {detected_emotion} today."
        else:
            response = "I'm sorry to hear that. Can I help you with this?"
        first_chat_after_hey = False  # Set the flag to False for subsequent chats
    else:
        if message.lower()=="work stress has been overwhelming deadlines and expectations are piling up":
            response = "Work stress can be challenging to deal with. How have you been coping with the stress so far?"
        elif message.lower()=="taking short break and refreshment":
            response = "Those are helpful strategies. It's great that you're taking breaks and having refreshment. Have you considered seeking additional support from a professional counselor or therapist?"
        elif message.lower()=="i am thinking of consoling of therapist":
            response = "Finding a counselor or therapist can be a positive step. You can start by asking your primary care physician for a referral or explore online directories like Psychology Today. It's important to find someone you feel comfortable with and who specializes in the areas you need support in."
        else:
            response = "Sorry I am still learning bot"

    return response

def detect_emotion():
    global detected_emotion
    # Perform face detection and emotion prediction
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray)

    # Initialize detected emotion as an empty string
    detected_emotion = ""

    # Check if any faces are detected
    if len(faces) > 0:
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)
            roi = roi_gray.astype('float') / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            # Predict emotion
            prediction = emotion_classifier.predict(roi)[0]
            emotion_label = emotion_labels[prediction.argmax()]

            # Store the detected emotion
            detected_emotion = emotion_label

    # Check if emotion is detected
    if detected_emotion is not None:
        # Keep the camera on for a certain duration
        camera_off_time = 5  # Change this value to the desired duration in seconds
        if time.time() - start_time >= camera_off_time:
            cap.release()
    else:
        # Emotion not detected, turn off the camera
        cap.release()

def start_emotion_detection():
    while True:
        detect_emotion()
        time.sleep(1)

if __name__ == '__main__':
    # Start emotion detection in a separate thread
    import threading
    emotion_thread = threading.Thread(target=start_emotion_detection)
    emotion_thread.start()

    app.run()

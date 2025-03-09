import cv2
import numpy as np
import os
import pickle
import argparse
from face_recognition import face_encodings, compare_faces

class FaceIDSystem:
    def __init__(self):
        self.known_encodings = []
        self.known_names = []
        self.data_file = "face_data.pkl"
        self.detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'rb') as f:
                data = pickle.load(f)
                self.known_encodings = data['encodings']
                self.known_names = data['names']

    def save_data(self):
        with open(self.data_file, 'wb') as f:
            pickle.dump({'encodings': self.known_encodings, 'names': self.known_names}, f)

    def capture_face(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise IOError("Cannot open webcam")

        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            return None

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) == 0:
            return None

        (x, y, w, h) = faces[0]
        face_img = frame[y:y+h, x:x+w]
        return cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)

    def enroll_user(self, name):
        face_img = self.capture_face()
        if face_img is None:
            print("No face detected!")
            return False

        encoding = face_encodings(face_img)
        if len(encoding) > 0:
            self.known_encodings.append(encoding[0])
            self.known_names.append(name)
            self.save_data()
            print(f"User {name} enrolled successfully!")
            return True
        return False

    def authenticate(self):
        face_img = self.capture_face()
        if face_img is None:
            return None

        encoding = face_encodings(face_img)
        if len(encoding) == 0:
            return None

        matches = compare_faces(self.known_encodings, encoding[0], tolerance=0.5)
        if True in matches:
            first_match_index = matches.index(True)
            return self.known_names[first_match_index]
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Face ID System')
    parser.add_argument('--enroll', help='Enroll a new user')
    parser.add_argument('--auth', action='store_true', help='Authenticate user')
    args = parser.parse_args()

    face_id = FaceIDSystem()

    if args.enroll:
        face_id.enroll_user(args.enroll)
    elif args.auth:
        user = face_id.authenticate()
        if user:
            print(f"Authenticated as {user}")
        else:
            print("Authentication failed")
    else:
        print("Please specify --enroll <name> or --auth")
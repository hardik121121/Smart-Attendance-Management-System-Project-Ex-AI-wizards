import cv2
import pickle
import face_recognition
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Load the dataset
with open('encoded_people.pickle', 'rb') as file:
    people = pickle.load(file)

font = ImageFont.truetype("arial.ttf", size=20)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame. Exiting.")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_location, face_encoding in zip(face_locations, face_encodings):
        name = "Unknown"
        for person_name, encodings in people.items():
            matches = face_recognition.compare_faces(encodings, face_encoding, tolerance=0.5)
            if any(matches):
                name = person_name
                break

        # Draw bounding box
        top, right, bottom, left = face_location
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(frame, name, (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    cv2.imshow("Webcam Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

import pickle
import face_recognition
from PIL import Image, ImageDraw, ImageFont
from tkinter import filedialog, Tk
import os
import csv
from datetime import datetime

# Load the dataset
with open('encoded_people.pickle', 'rb') as file:
    people = pickle.load(file)

# Select an image file
print("Select an image for face recognition.")
root = Tk()
root.withdraw()
image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
if not image_path:
    print("No image selected. Exiting.")
    exit(0)

# CSV file to track attendance
csv_file = "attendance.csv"
if not os.path.exists(csv_file):
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Timestamp"])  # Add headers

# Load and process the image
image = face_recognition.load_image_file(image_path)
face_locations = face_recognition.face_locations(image)
face_encodings = face_recognition.face_encodings(image, face_locations)

if not face_encodings:
    print("No faces detected.")
    exit(0)

# Draw and label detected faces
image_pil = Image.fromarray(image)
draw = ImageDraw.Draw(image_pil)
font = ImageFont.truetype("arial.ttf", size=20)

recognized_names = set()  # To avoid duplicate entries in the CSV

for face_location, face_encoding in zip(face_locations, face_encodings):
    top, right, bottom, left = face_location
    name = "Unknown"
    color = "red"  # Default color for unidentified faces

    # Compare with known faces
    for person_name, encodings in people.items():
        matches = face_recognition.compare_faces(encodings, face_encoding, tolerance=0.5)
        if any(matches):
            name = person_name
            color = "green"  # Change to green for identified faces
            break

    # Draw the face bounding box
    draw.rectangle([(left, top), (right, bottom)], outline=color, width=3)

    # Draw name box and text
    text_bbox = draw.textbbox((0, 0), name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    draw.rectangle([(left, bottom), (left + text_width, bottom + text_height + 5)], fill=color)
    draw.text((left, bottom), name, fill="white", font=font)

    # If identified, record attendance in CSV
    if name != "Unknown" and name not in recognized_names:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, timestamp])
        recognized_names.add(name)

# Show the labeled image
image_pil.show()

print(f"Attendance has been marked in {csv_file}.")

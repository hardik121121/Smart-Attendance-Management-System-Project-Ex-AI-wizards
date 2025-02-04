from flask import Flask, render_template, request, redirect, url_for, flash, send_file, Response
import os
import pickle
import face_recognition
import numpy as np
import cv2
import csv
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For flash messages
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

STUDENT_DIR = 'people'  # Directory where student images are stored
ATTENDANCE_FILE = 'attendance.csv'

# Load encoded data
if os.path.exists('encoded_people.pickle'):
    with open('encoded_people.pickle', 'rb') as file:
        people = pickle.load(file)
else:
    people = {}

# Ensure attendance.csv exists
if not os.path.exists(ATTENDANCE_FILE):
    with open(ATTENDANCE_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Timestamp"])  # Headers for the file


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/add_person', methods=['GET', 'POST'])
def add_person():
    if request.method == 'POST':
        name = request.form['name']
        image_file = request.files['image']

        if not name or not image_file:
            flash("Name and image are required!")
            return redirect(request.url)

        person_dir = os.path.join(STUDENT_DIR, name)
        if not os.path.exists(person_dir):
            os.makedirs(person_dir)

        image_path = os.path.join(person_dir, image_file.filename)
        image_file.save(image_path)

        # Process the image
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)

        if not face_encodings:
            os.remove(image_path)
            flash("No face detected in the uploaded image. Try again!")
        else:
            encoding = face_encodings[0]
            if name in people:
                people[name].append(encoding)
            else:
                people[name] = [encoding]

            # Remove duplicate encodings
            unique_faces = np.unique(np.array(people[name]), axis=0)
            people[name] = unique_faces.tolist()

            # Save updated data
            with open('encoded_people.pickle', 'wb') as file:
                pickle.dump(people, file)
            flash(f"{name} successfully added with {len(unique_faces)} unique faces!")

        return redirect(url_for('home'))

    return render_template('add_person.html')


@app.route('/recognize_image', methods=['GET', 'POST'])
def recognize_image():
    if request.method == 'POST':
        image_file = request.files['image']
        if not image_file:
            flash("Image is required!")
            return redirect(request.url)

        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
        image_file.save(image_path)

        # Load and process image
        image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        image_pil = Image.fromarray(image)
        draw = ImageDraw.Draw(image_pil)

        # Load font
        font_path = "arial.ttf"
        try:
            font = ImageFont.truetype(font_path, size=20)
        except IOError:
            font = ImageFont.load_default()

        recognized_names = set()  # To avoid duplicate entries in attendance

        for face_location, face_encoding in zip(face_locations, face_encodings):
            top, right, bottom, left = face_location
            name = "Unknown"

            for person_name, encodings in people.items():
                matches = face_recognition.compare_faces(encodings, face_encoding, tolerance=0.5)
                if any(matches):
                    name = person_name
                    break

            recognized_names.add(name)

            # Draw bounding box and label
            draw.rectangle([(left, top), (right, bottom)], outline="green" if name != "Unknown" else "red", width=3)
            
            # Text background
            text_bbox = draw.textbbox((0, 0), name, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            draw.rectangle(
                [(left, bottom), (left + text_width, bottom + text_height + 5)],
                fill="green" if name != "Unknown" else "red"
            )
            draw.text((left, bottom), name, fill="white", font=font)

        # Mark attendance in CSV
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(ATTENDANCE_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            for name in recognized_names:
                if name != "Unknown":
                    writer.writerow([name, timestamp])

        # Save result image
        result_path = os.path.join(app.config['UPLOAD_FOLDER'], f"result_{image_file.filename}")
        image_pil.save(result_path)

        return render_template('results.html', image=result_path, recognized_names=list(recognized_names))

    return render_template('recognize_image.html')


@app.route('/student')
def student_dashboard():
    all_students = os.listdir(STUDENT_DIR) if os.path.exists(STUDENT_DIR) else []
    
    # Read attendance records
    present_students = set()
    if os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            for row in reader:
                present_students.add(row[0])  # Name is in the first column

    student_data = [{"name": student, "status": "Present" if student in present_students else "Absent"} for student in all_students]

    return render_template('student_dashboard.html', students=student_data)


### **Webcam Face Recognition**
def generate_frames():
    cap = cv2.VideoCapture(0)

    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            recognized_names = set()

            for face_location, face_encoding in zip(face_locations, face_encodings):
                name = "Unknown"
                for person_name, encodings in people.items():
                    matches = face_recognition.compare_faces(encodings, face_encoding, tolerance=0.5)
                    if any(matches):
                        name = person_name
                        break

                recognized_names.add(name)

                # Draw bounding box
                top, right, bottom, left = face_location
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, name, (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            # Mark attendance
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(ATTENDANCE_FILE, 'a', newline='') as file:
                writer = csv.writer(file)
                for name in recognized_names:
                    if name != "Unknown":
                        writer.writerow([name, timestamp])

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()


@app.route('/webcam_feed')
def webcam_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/webcam_recognition')
def webcam_recognition():
    return render_template('webcam_recognition.html')

@app.route('/download_csv')
def download_csv():
    return send_file("attendance.csv",as_attachment=True,mimetype="text/csv",download_name="attendance.csv")


if __name__ == '__main__':
    app.run(debug=True)

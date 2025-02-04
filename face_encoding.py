import pickle
import os
import face_recognition

dir = os.getcwd()
people = {}

people_dir = os.path.join(dir, 'people')
if not os.path.isdir(people_dir):
    print("No 'people' folder found.")
    exit(0)

for person in os.listdir(people_dir):
    person_dir = os.path.join(people_dir, person)
    if not os.path.isdir(person_dir):
        continue
    person_faces = []
    for photo in os.listdir(person_dir):
        if not photo.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
        image_path = os.path.join(person_dir, photo)
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)
        if face_encodings:
            person_faces.append(face_encodings[0])
    if person_faces:
        people[person] = person_faces
        print(f"{len(person_faces)} faces encoded for {person}.")
    else:
        print(f"No faces found for {person}.")

# Save the dataset
with open('encoded_people.pickle', 'wb') as file:
    pickle.dump(people, file)
    print("All encodings saved successfully!")

import pickle
import os
import face_recognition
import numpy as np
from tkinter import filedialog, Tk

dir = os.getcwd()

# Load existing data or initialize an empty dictionary
if os.path.exists('encoded_people.pickle'):
    with open('encoded_people.pickle', 'rb') as file:
        people = pickle.load(file)
else:
    people = {}

print("Register a new person by providing their name and selecting an image.")
new_person_name = input("Enter the new person's name: ")

people_dir = os.path.join(dir, 'people')
if not os.path.isdir(people_dir):
    os.makedirs(people_dir)
    print(f"'people' folder created in {people_dir}")

# Create a folder for the new person if it doesn't exist
person_dir = os.path.join(people_dir, new_person_name)
if not os.path.isdir(person_dir):
    os.makedirs(person_dir)
    print(f"Folder created for {new_person_name} in {person_dir}")

# Select an image for the new person
root = Tk()
root.withdraw()
print("Please select an image of the person.")
image_path = filedialog.askopenfilename(
    title="Select Image",
    filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
)

if not image_path:
    print("No image selected. Exiting.")
    exit(0)

# Copy the selected image to the person's folder
image_name = os.path.basename(image_path)
saved_image_path = os.path.join(person_dir, image_name)
with open(image_path, 'rb') as source_file:
    with open(saved_image_path, 'wb') as dest_file:
        dest_file.write(source_file.read())
print(f"Image saved in {saved_image_path}")

# Process the image and encode faces
image = face_recognition.load_image_file(saved_image_path)
face_encodings = face_recognition.face_encodings(image)

if not face_encodings:
    print("No faces were found in the provided image. Please try with another image.")
    os.remove(saved_image_path)  # Remove the image since it's invalid
else:
    print(f"{len(face_encodings)} face(s) found for {new_person_name}.")
    person_faces = face_encodings[0]  # Take the first encoding

    # Add or update the encoding in the dataset
    if new_person_name in people:
        people[new_person_name].append(person_faces)
    else:
        people[new_person_name] = [person_faces]

    # Remove duplicate encodings
    unique_faces = np.unique(np.array(people[new_person_name]), axis=0)
    people[new_person_name] = unique_faces.tolist()
    print(f"Updated {new_person_name}'s profile with {len(unique_faces)} unique faces.")

    # Save the updated dataset
    with open('encoded_people.pickle', 'wb') as file:
        pickle.dump(people, file)
    print("Updated dataset saved successfully!")

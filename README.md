### 📌 **README.md** - Smart Attendance Management System  

# 🏫 Smart Attendance Management System  

A **Face Recognition-based Attendance System** that automates attendance tracking using **Flask, OpenCV, and Face Recognition**. This project enables users to **register new individuals** and **recognize faces from uploaded images** for attendance marking.  

---

## ✨ **Features**  

✔ **Register New People**: Upload an image and store face encodings.  
✔ **Recognize Faces**: Identify registered individuals in an image.  
✔ **Flask Web Interface**: Simple UI to interact with the system.  
✔ **Persistent Data Storage**: Uses **pickle** for storing face encodings.  
✔ **Bounding Box with Names**: Displays recognized names on detected faces.  

---

## 🏗 **Project Structure**  

```
📂 smart_attendance/
│── 📁 people/                 # Stores user images in named folders
│── 📁 static/uploads/         # Stores uploaded & processed images
│── 📜 app.py                  # Main Flask application
│── 📜 add_new_person.py       # Registers a new person
│── 📜 recognize_person.py     # Recognizes faces in an image
│── 📜 encoded_people.pickle   # Stores face encodings
│── 📜 requirements.txt        # Dependencies
│── 📜 README.md               # Documentation (You're here! 🎉)
│── 📁 templates/              # HTML Templates for Flask UI
│     ├── index.html           # Home page
│     ├── add_person.html      # Registration page
│     ├── recognize_image.html # Face recognition page
│     ├── results.html         # Results page
```

---

## ⚙ **How It Works?**  

1️⃣ **User Registration:**  
   - User uploads an image via the **Flask UI**.  
   - The system extracts facial features using `face_recognition`.  
   - The encoding is stored in `encoded_people.pickle`.  

2️⃣ **Face Recognition:**  
   - User uploads an image with faces.  
   - The system compares face encodings with stored data.  
   - Recognized faces are **highlighted with names in a bounding box**.  

3️⃣ **Data Storage:**  
   - All face encodings are stored persistently using **pickle**.  
   - Duplicate encodings are removed using **NumPy**.  

---

## 🛠 **Setup Instructions**  

### ✅ Prerequisites  
- Python 3.8+  
- Flask  
- OpenCV  
- face_recognition (Requires dlib)  

### 📥 Installation  

1️⃣ **Clone the Repository**  
```bash
git clone https://github.com/your-repo/smart-attendance.git
cd smart-attendance
```

2️⃣ **Create a Virtual Environment (Optional, Recommended)**  
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

3️⃣ **Install Dependencies**  
```bash
pip install -r requirements.txt
```

4️⃣ **Run the Flask App**  
```bash
python app.py
```

5️⃣ **Access the Web App**  
Open a browser and visit **http://127.0.0.1:5000/**  

---

## 📚 **Libraries Used & Their Role**  

| Library              | Purpose 📌 |
|----------------------|-----------|
| `Flask`             | Web framework for the UI 🌐 |
| `face_recognition`  | Facial feature extraction & recognition 🤖 |
| `OpenCV`            | Image processing & face detection 📸 |
| `PIL (Pillow)`      | Image drawing for bounding boxes 🖼 |
| `NumPy`             | Optimizing face encoding storage 🔢 |
| `Pickle`            | Saving and loading face encodings 🔐 |
| `os` & `shutil`     | File handling for storing images 📂 |

---

## 🛠 **How to Contribute?**  

1️⃣ **Fork the repository**  
2️⃣ **Create a new branch** (`git checkout -b feature-branch`)  
3️⃣ **Commit changes** (`git commit -m "Added feature XYZ"`)  
4️⃣ **Push to GitHub** (`git push origin feature-branch`)  
5️⃣ **Open a Pull Request (PR)**  

---

## 🎯 **Future Enhancements**  

🚀 **Real-time Face Recognition** using a webcam.  
📊 **Database Integration** (MongoDB/PostgreSQL).  
📌 **Mobile App Integration** for remote attendance marking.  

---

## 👥 **Team Members**  

- **Hardik Arora** - End-to-End Developer 🧑‍💻  
- **Hemant Prajapati** - Backend Tester 🧑‍💻  
- **Harsh Raj** - UI/UX Designer 🎨  
- **Divyanshu Rajoria** - UI/UX Designer 🎨  
- **Amitabh Singh** - Database Admin 🗄  
- **Shiven Rastogi** - Tester 🛠  
- **Nikita Chaudhary** - Tester 🛠  

---

### 📧 **Have Questions?**  

Contact us at **hardikarora483@gmail.com** or create an **issue** in GitHub.  

🚀 **Happy Coding!** 😊  

---

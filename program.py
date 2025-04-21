import face_recognition
import cv2
import numpy as np
import os
from datetime import datetime
from pymongo import MongoClient
import matplotlib.pyplot as plt

# 📌 MongoDB Setup
client = MongoClient("mongodb://localhost:27017")
db = client["attendance_system"]
attendance_collection = db["attendance_records"]
students_collection = db["students"]
detection_logs_collection = db["detection_logs"]
accuracy_logs_collection = db["accuracy_logs"]

# 📂 Load known faces
known_face_encodings = []
known_face_names = []

photo_dir = "photos"
for filename in os.listdir(photo_dir):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        path = os.path.join(photo_dir, filename)
        image = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_face_encodings.append(encodings[0])
            name = os.path.splitext(filename)[0].lower()
            known_face_names.append(name)
            students_collection.update_one(
                {"name": name},
                {"$set": {"name": name, "image_path": path}},
                upsert=True
            )

students = known_face_names.copy()

# 🎥 Initialize webcam
video_capture = cv2.VideoCapture(0)
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

# 🎯 Accuracy Tracking
correct = 0
incorrect = 0

while True:
    _, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

            # ✅ Log accuracy
            is_correct = name in known_face_names
            if is_correct:
                correct += 1
            else:
                incorrect += 1

            detection_logs_collection.insert_one({
                "detected_name": name,
                "actual_name": name if is_correct else "Unknown",
                "timestamp": datetime.now(),
                "is_correct": is_correct
            })

            if is_correct and name in students:
                students.remove(name)
                attendance_collection.insert_one({
                    "name": name,
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "time": datetime.now().strftime("%H:%M:%S")
                })

    # 🖼️ Display video feed
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6),
                    cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

    cv2.imshow("Attendance System", frame)

    # 🛑 Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 🧮 Final Accuracy/Loss Computation
total = correct + incorrect
accuracy = correct / total if total else 0
loss = 1 - accuracy

# 📝 Save accuracy stats to MongoDB
accuracy_logs_collection.insert_one({
    "timestamp": datetime.now(),
    "correct": correct,
    "incorrect": incorrect,
    "accuracy": accuracy,
    "loss": loss
})

# 🧼 Cleanup
video_capture.release()
cv2.destroyAllWindows()

print(f"\n✅ Final Accuracy: {accuracy*100:.2f}%")
print(f"❌ Final Loss: {loss*100:.2f}%")

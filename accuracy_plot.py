from pymongo import MongoClient
import matplotlib.pyplot as plt

# 📌 MongoDB Setup
client = MongoClient("mongodb://localhost:27017")  # Replace with your Atlas URI if needed
db = client["attendance_system"]
detection_logs_collection = db["detection_logs"]

# 📝 Fetch all detection logs
logs = detection_logs_collection.find()

# 🧮 Calculate accuracy
correct = 0
total = 0
accuracies = []
times = []

for log in logs:
    total += 1
    if log["is_correct"]:
        correct += 1

    # Track accuracy for each log
    accuracies.append(correct / total * 100)
    times.append(log["time"])

# 📊 Plot the accuracy graph
plt.figure(figsize=(10, 6))
plt.plot(times, accuracies, marker='o', color='b')
plt.title("Face Recognition Accuracy Over Time")
plt.xlabel("Time")
plt.ylabel("Accuracy (%)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

# Show plot
plt.show()

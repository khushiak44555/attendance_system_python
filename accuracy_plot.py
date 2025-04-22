from pymongo import MongoClient
import matplotlib.pyplot as plt

# 📌 MongoDB Setup
client = MongoClient("mongodb://localhost:27017")  # Update if using a remote DB
db = client["attendance_system"]
detection_logs_collection = db["detection_logs"]

# 📝 Fetch all detection logs
logs = detection_logs_collection.find()

# 🧮 Calculate accuracy
correct = 0
total = 0
accuracies = []
times = []

for idx, log in enumerate(logs, start=1):
    if "timestamp" not in log:
        print(f"⚠️ Log #{idx} is missing 'timestamp' field: {log}")
        continue  # Skip logs with missing 'timestamp'

    total += 1
    if log.get("is_correct"):
        correct += 1

    # Track accuracy and corresponding timestamp
    accuracies.append(correct / total * 100)
    times.append(log["timestamp"])

# 📊 Plot the accuracy graph
if times and accuracies:
    plt.figure(figsize=(10, 6))
    plt.plot(times, accuracies, marker='o', color='b')
    plt.title("Face Recognition Accuracy Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel("Accuracy (%)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
else:
    print("❌ No valid logs with 'timestamp' found to plot.")

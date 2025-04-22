from pymongo import MongoClient
from datetime import datetime
import matplotlib.pyplot as plt

# MongoDB connection
client = MongoClient("mongodb://localhost:27017")
db = client["attendance_system"]
logs = db["detection_logs"]

# Fetch and sort logs by timestamp
records = list(logs.find().sort("timestamp", 1))

# Prepare data
timestamps = []
accuracy_vals = []
loss_vals = []

correct = 0
total = 0

for i, record in enumerate(records, start=1):
    is_correct = record.get("is_correct", False)
    timestamp = record.get("timestamp")

    if timestamp is None:
        continue

    total += 1
    if is_correct:
        correct += 1

    accuracy = correct / total
    loss = 1 - accuracy

    timestamps.append(timestamp.strftime("%H:%M:%S"))
    accuracy_vals.append(accuracy)
    loss_vals.append(loss)

# Plotting
if timestamps:
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, accuracy_vals, marker='o', label='Accuracy', color='green')
    plt.plot(timestamps, loss_vals, marker='x', label='Loss', color='red')
    plt.xlabel("Timestamp")
    plt.ylabel("Rate")
    plt.title("Face Detection Accuracy and Loss Over Time")
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
else:
    print("❌ No valid detection logs found.")

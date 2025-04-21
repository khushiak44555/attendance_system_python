import matplotlib.pyplot as plt
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["attendance_system"]
accuracy_logs_collection = db["accuracy_logs"]

# Fetch data
records = list(accuracy_logs_collection.find())
timestamps = [r["timestamp"].strftime("%H:%M:%S") for r in records]
accuracy_vals = [r["accuracy"] for r in records]
loss_vals = [r["loss"] for r in records]

# Plotting
plt.figure(figsize=(10, 5))
plt.plot(timestamps, accuracy_vals, marker='o', label="Accuracy", color="green")
plt.plot(timestamps, loss_vals, marker='x', label="Loss", color="red")
plt.xlabel("Timestamp")
plt.ylabel("Rate")
plt.title("Face Recognition Accuracy vs Loss Over Time")
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

from pymongo import MongoClient
from datetime import datetime
import matplotlib.pyplot as plt

# 📌 Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["attendance_system"]
attendance_collection = db["attendance_records"]

# 📅 Dates to analyze
dates = attendance_collection.distinct("date")

accuracy_results = []

for date in dates:
    total_detected = 10  # Simulate total faces detected (replace this with actual log if available)
    
    # 🎯 Count correct matches for the day
    correct_matches = attendance_collection.count_documents({"date": date})

    accuracy = (correct_matches / total_detected) * 100 if total_detected else 0
    accuracy_results.append({
        "date": date,
        "accuracy": accuracy,
        "correct": correct_matches,
        "total": total_detected
    })

# 📊 Data for plotting
dates = [result['date'] for result in accuracy_results]
accuracies = [result['accuracy'] for result in accuracy_results]
corrects = [result['correct'] for result in accuracy_results]
totals = [result['total'] for result in accuracy_results]

# 📈 Plot accuracy over time
plt.figure(figsize=(10, 6))
plt.plot(dates, accuracies, marker='o', color='green', label="Accuracy %")
plt.title("Face Recognition Accuracy Over Time")
plt.xlabel("Date")
plt.ylabel("Accuracy (%)")
plt.ylim(0, 100)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("accuracy_chart.png")
plt.show()

# 📊 Bar Chart for Total vs Correct
plt.figure(figsize=(10, 6))
bar_width = 0.35
index = range(len(dates))

plt.bar(index, totals, bar_width, label='Total Detected', color='orange')
plt.bar([i + bar_width for i in index], corrects, bar_width, label='Correct Matches', color='blue')
plt.xticks([i + bar_width / 2 for i in index], dates)
plt.title("Total vs Correct Matches")
plt.xlabel("Date")
plt.ylabel("Count")
plt.legend()
plt.tight_layout()
plt.savefig("match_stats.png")
plt.show()

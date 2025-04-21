from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")  # Or your Atlas URI
db = client["attendance_system"]
attendance_collection = db["attendance_records"]

@app.route("/", methods=["GET"])
def index():
    # Optional filters
    name_filter = request.args.get("name", "")
    date_filter = request.args.get("date", "")

    query = {}
    if name_filter:
        query["name"] = {"$regex": name_filter, "$options": "i"}
    if date_filter:
        query["date"] = date_filter

    records = list(attendance_collection.find(query).sort("time", -1))
    return render_template("index.html", records=records)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='/')
CORS(app)

DATA_PATH = os.path.join(os.path.dirname(__file__), '../data/tasks.json')

# Load tasks from JSON
if os.path.exists(DATA_PATH):
    with open(DATA_PATH, 'r') as f:
        tasks = json.load(f)
else:
    tasks = []

def save_tasks():
    with open(DATA_PATH, 'w') as f:
        json.dump(tasks, f, indent=2)

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def add_task():
    task = request.json
    tasks.append(task)
    save_tasks()
    return jsonify({"status": "success", "task": task})

@app.route("/tasks/<int:index>", methods=["PUT"])
def update_task(index):
    if 0 <= index < len(tasks):
        tasks[index] = request.json
        save_tasks()
        return jsonify({"status": "success", "task": tasks[index]})
    return jsonify({"status": "error", "message": "Task not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
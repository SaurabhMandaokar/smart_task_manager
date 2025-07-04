from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from notion_client import Client
import os

# Flask setup
app = Flask(__name__, static_folder='../frontend', static_url_path='/')
CORS(app)

# Notion API setup
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")  # safer than hardcoding
DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")

notion = Client(auth=NOTION_TOKEN)

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/tasks", methods=["GET"])
def get_tasks():
    response = notion.databases.query(database_id=DATABASE_ID)
    tasks = []

    for result in response["results"]:
        props = result["properties"]
        tasks.append({
            "id": result["id"],
            "title": props["Title"]["title"][0]["text"]["content"] if props["Title"]["title"] else "",
            "dueDate": props["Due Date"]["date"]["start"] if props["Due Date"]["date"] else "",
            "description": props["Description"]["rich_text"][0]["text"]["content"] if props["Description"]["rich_text"] else "",
            "priority": props["Priority"]["select"]["name"] if props["Priority"]["select"] else "",
            "status": props["Status"]["select"]["name"] if props["Status"]["select"] else ""
        })

    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def add_task():
    task = request.json
    notion.pages.create(
        parent={"database_id": DATABASE_ID},
        properties={
            "Title": {"title": [{"text": {"content": task["title"]}}]},
            "Due Date": {"date": {"start": task["dueDate"]}},
            "Description": {"rich_text": [{"text": {"content": task["description"]}}]},
            "Priority": {"select": {"name": task["priority"]}},
            "Status": {"select": {"name": task["status"]}}
        }
    )
    return jsonify({"status": "success"})

@app.route("/tasks/<string:page_id>", methods=["PUT"])
def update_task(page_id):
    task = request.json
    notion.pages.update(
        page_id=page_id,
        properties={
            "Title": {"title": [{"text": {"content": task["title"]}}]},
            "Due Date": {"date": {"start": task["dueDate"]}},
            "Description": {"rich_text": [{"text": {"content": task["description"]}}]},
            "Priority": {"select": {"name": task["priority"]}},
            "Status": {"select": {"name": task["status"]}}
        }
    )
    return jsonify({"status": "updated"})

if __name__ == "__main__":
    app.run(debug=True)
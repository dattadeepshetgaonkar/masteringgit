import json
import os
import uuid
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory

app = Flask(__name__)
PUBLIC_DIR = os.path.join(os.path.dirname(__file__), "public")
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

# On Vercel, only /tmp is writable. Locally, we use a data file next to app.py.
DATA_FILE = "/tmp/tasks.json" if os.environ.get("VERCEL") else os.path.join(
    os.path.dirname(__file__), "tasks.json"
)


def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


@app.route("/style.css")
def styles():
    # On Vercel, files in public/ are served automatically by the CDN.
    # Locally, Flask needs this route to serve the same file at the same path.
    return send_from_directory(PUBLIC_DIR, "style.css")


@app.route("/")
def index():
    tasks = load_tasks()
    filter_by = request.args.get("filter", "all")

    if filter_by == "active":
        visible = [t for t in tasks if not t["done"]]
    elif filter_by == "done":
        visible = [t for t in tasks if t["done"]]
    else:
        visible = tasks

    priority_rank = {"high": 0, "medium": 1, "low": 2}
    visible.sort(key=lambda t: (t["done"], priority_rank.get(t["priority"], 1)))

    stats = {
        "total": len(tasks),
        "done": sum(1 for t in tasks if t["done"]),
        "active": sum(1 for t in tasks if not t["done"]),
    }

    return render_template("index.html", tasks=visible, stats=stats, filter_by=filter_by)


@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    priority = request.form.get("priority", "medium")

    if not title:
        flash("Task title can't be empty.", "error")
        return redirect(url_for("index"))

    tasks = load_tasks()
    tasks.append({
        "id": str(uuid.uuid4()),
        "title": title,
        "priority": priority if priority in ("low", "medium", "high") else "medium",
        "done": False,
        "created_at": datetime.utcnow().isoformat(),
    })
    save_tasks(tasks)
    flash("Task added.", "success")
    return redirect(url_for("index"))


@app.route("/toggle/<task_id>", methods=["POST"])
def toggle_task(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = not t["done"]
            break
    save_tasks(tasks)
    return redirect(url_for("index"))


@app.route("/delete/<task_id>", methods=["POST"])
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    flash("Task deleted.", "success")
    return redirect(url_for("index"))


@app.route("/api/tasks")
def api_tasks():
    """Simple JSON API endpoint, handy for testing or future frontend work."""
    return {"tasks": load_tasks()}


if __name__ == "__main__":
    app.run(debug=True)

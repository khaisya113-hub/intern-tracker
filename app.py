from flask import Flask, render_template, request, redirect, url_for
from database import init_db, get_all_tasks, add_task, update_task_status, delete_task, get_task

app = Flask(__name__)

@app.route("/")
def index():
    tasks = get_all_tasks()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    description = request.form.get("description")
    if title:
        add_task(title, description)
    return redirect(url_for("index"))

@app.route("/update/<int:task_id>", methods=["POST"])
def update(task_id):
    status = request.form.get("status")
    update_task_status(task_id, status)
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete(task_id):
    delete_task(task_id)
    return redirect(url_for("index"))

@app.route("/edit/<int:task_id>")
def edit(task_id):
    task = get_task(task_id)
    return render_template("edit.html", task=task)

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
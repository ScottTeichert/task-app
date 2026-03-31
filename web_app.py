import os
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)

database_url = os.getenv("DATABASE_URL", "sqlite:///project.db")

if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_urlSE_URI"] = os.getenv("DATABASE_URL", "sqlite:///project.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-only-secret-key")
app.config["DEBUG"] = os.getenv("FLASK_DEBUG", "False").lower() == "true"

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    tasks = db.relationship("Task", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    owner = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(50), nullable=False)
    details = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default="Not Started")
    prospect_id = db.Column(db.String(50), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<Task {self.title}>"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "owner": self.owner,
            "due_date": self.due_date,
            "priority": self.priority,
            "details": self.details,
            "status": self.status,
            "prospect_id": self.prospect_id,
            "user_id": self.user_id,
        }


def login_required(f):
    @wraps(f)
    def wrapped_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapped_function


@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("list_tasks"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already exists. Try another."

        hashed_password = generate_password_hash(password)

        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect(url_for("list_tasks"))

        return "Invalid username or password."

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/tasks")
@login_required
def list_tasks():
    tasks = Task.query.filter_by(user_id=session["user_id"]).all()
    return render_template("tasks.html", tasks=tasks, username=session.get("username"))


@app.route("/add", methods=["GET", "POST"])
@login_required
def add_task():
    if request.method == "POST":
        new_task = Task(
            title=request.form.get("title"),
            owner=request.form.get("owner"),
            due_date=request.form.get("due_date"),
            priority=request.form.get("priority"),
            details=request.form.get("details"),
            status=request.form.get("status") or "Not Started",
            prospect_id=request.form.get("prospect_id"),
            user_id=session["user_id"],
        )

        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for("list_tasks"))

    return render_template("add.html")


@app.route("/edit/<int:item_id>", methods=["GET", "POST"])
@login_required
def edit_task(item_id):
    task = Task.query.filter_by(id=item_id, user_id=session["user_id"]).first_or_404()

    if request.method == "POST":
        task.title = request.form.get("title")
        task.owner = request.form.get("owner")
        task.due_date = request.form.get("due_date")
        task.priority = request.form.get("priority")
        task.details = request.form.get("details")
        task.status = request.form.get("status")
        task.prospect_id = request.form.get("prospect_id")

        db.session.commit()
        return redirect(url_for("list_tasks"))

    return render_template("edit.html", task=task)


@app.route("/delete/<int:item_id>")
@login_required
def delete_task(item_id):
    task = Task.query.filter_by(id=item_id, user_id=session["user_id"]).first_or_404()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("list_tasks"))


@app.route("/api/v1/tasks", methods=["GET"])
@login_required
def api_list_tasks():
    tasks = Task.query.filter_by(user_id=session["user_id"]).all()
    return jsonify([task.to_dict() for task in tasks])


@app.route("/api/v1/tasks/<int:item_id>", methods=["GET"])
@login_required
def api_get_task(item_id):
    task = Task.query.filter_by(id=item_id, user_id=session["user_id"]).first()

    if task is None:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task.to_dict())


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run()
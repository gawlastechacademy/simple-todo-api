from flask import jsonify
from datetime import datetime

from src.database import db
from src.models.task import Task, status_correct
from src.models.user import User
from src.services.user_service import get_current_user


def get_all_todo():
    user = get_current_user()
    if not user.is_administrator():
        return jsonify({"description": "unauthorized"}), 401
    tasks = Task.query.all()
    tasks_dict = [task.to_dict() for task in tasks]

    return jsonify(tasks_dict), 200


def add_single_todo(title, description, status, due_date):
    # check errors
    user = get_current_user()
    user_id = user.user_id

    if not status_correct(status):
        return jsonify({"description": "invalid status"}), 400

    create_time = datetime.now()

    new_task = Task(
        user_id=user_id,
        title=title,
        description=description,
        status=status,
        create_time=create_time,
        due_date=due_date
    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify(new_task.to_dict()), 201


def get_single_todo(task_id):
    user = get_current_user()
    task = Task.query.get(task_id)

    if task is None:
        return jsonify({"description": f"task '{task_id}' not found"}), 404

    if task.user_id != user.user_id and not user.is_administrator():
        return jsonify({"description": "Unauthorized"}), 401

    return jsonify(task.to_dict()), 200


def delete_single_todo(task_id):
    task = Task.query.get(task_id)
    user = get_current_user()

    if task is None:
        return jsonify({"description": f"task '{task_id}' not found"}), 404

    if task.user_id != user.user_id and not user.is_administrator():
        return jsonify({"description": "unauthorized"}), 401

    db.session.delete(task)
    db.session.commit()

    return jsonify({"description": "task deleted"}), 200


def update_single_todo(data, task_id):
    task = Task.query.get(task_id)
    user = get_current_user()

    # check errors
    if task is None:
        return jsonify({"description": f"task '{task_id}' not found"}), 404

    if "status" in data.keys() and not status_correct(data["status"]):
        return jsonify({"description": "invalid status"}), 404

    if task.user_id != user.user_id and not user.is_administrator():
        return jsonify({"description": "unauthorized"}), 401

    # update task fields
    if "title" in data.keys():
        task.title = data["title"]
    if "description" in data.keys():
        task.description = data["description"]
    if "status" in data.keys():
        task.status = data["status"]
    if "due_date" in data.keys():
        task.due_date = data["due_date"]

    db.session.commit()

    return jsonify(task.to_dict()), 200


def get_user_todos(user_id):
    user = User.query.get(user_id)
    user_logged = get_current_user()
    if user is None:
        return jsonify({"description": "invalid user id"}), 409

    if user.user_id != user_logged.user_id and not user_logged.is_administrator():
        return jsonify({"description": "unauthorized"}), 401

    all_tasks = Task.query.filter(Task.user_id == user_id).all()
    all_tasks_dict = [task.to_dict() for task in all_tasks]

    return jsonify(all_tasks_dict), 200

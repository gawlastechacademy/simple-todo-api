from flask import Blueprint, request
import src.services.todo_service as todo_service
from flask_jwt_extended import jwt_required

todo_app = Blueprint("todo", __name__)


@todo_app.route("/todos/", methods=["GET"])
@jwt_required()
def list_todos():
    return todo_service.get_all_todo()


@todo_app.route("/todos/", methods=["POST"])
@jwt_required()
def add_todo():
    post_data = request.json
    title = post_data["title"]
    description = post_data["description"]
    status = post_data["status"]
    do_time = post_data["do_time"]
    return todo_service.add_single_todo(title, description, status, do_time)


@todo_app.route("/todos/<task_id>", methods=["GET"])
@jwt_required()
def get_single_task(task_id):
    return todo_service.get_single_todo(task_id)


@todo_app.route("/todos/<task_id>", methods=["DELETE"])
@jwt_required()
def delete_single_task(task_id):
    return todo_service.delete_single_todo(task_id)


@todo_app.route("/todos/<task_id>", methods=["PUT"])
@jwt_required()
def update_single_task(task_id):
    post_request = request.json
    return todo_service.update_single_todo(post_request, task_id)


@todo_app.route("/users/<user_id>/todos/", methods=["GET"])
@jwt_required()
def todos_user(user_id):
    return todo_service.get_user_todos(user_id)

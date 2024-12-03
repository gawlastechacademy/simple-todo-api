import os
from flask import Flask, request
import db_init
from dotenv import load_dotenv
import src.services.todo_service as todo_service
import src.services.user_service as user_service

# load .env file to environment
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.route("/register/", methods=["POST"])
def register():
    post_data = request.json
    user_name = post_data["user"]
    user_password = post_data["password"]
    user_admin = post_data["admin"]
    return user_service.create_user(user_name, user_password, user_admin)


@app.route("/login/", methods=["POST"])
def login():
    post_data = request.json
    user_name = post_data["user"]
    user_password = post_data["password"]
    return user_service.login(user_name, user_password)


@app.route("/todos/", methods=["GET"])
def list_todos():
    return todo_service.get_all_todo()


@app.route("/todos/", methods=["POST"])
def add_todo():
    post_data = request.json
    title = post_data["title"]
    description = post_data["description"]
    status = post_data["status"]
    do_time = post_data["do_time"]
    user_id = post_data["user_id"]
    return todo_service.add_single_todo(user_id, title, description, status, do_time)


@app.route("/todos/<task_id>", methods=["GET"])
def get_single_task(task_id):
    return todo_service.get_single_todo(task_id)


@app.route("/todos/<task_id>", methods=["DELETE"])
def delete_single_task(task_id):
    return todo_service.delete_single_todo(task_id)


@app.route("/todos/<task_id>", methods=["PUT"])
def update_single_task(task_id):
    post_request = request.json

    return todo_service.update_single_todo(post_request, task_id)


# return all tasks from one user
@app.route("/users/<user_id>/todos/", methods=["GET"])
def todos_user(user_id):
    return todo_service.get_user_todos(user_id)


if __name__ == '__main__':
    db_init.check_and_create_db()
    app.run(host='0.0.0.0', port=8080)

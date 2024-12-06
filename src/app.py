from flask import Flask, request
import src.services.todo_service as todo_service
import src.services.user_service as user_service
from src.database import db
from flask_jwt_extended import JWTManager, jwt_required

app = Flask(__name__)
app.config.from_object("config.Config")
db.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()


@app.route("/register/", methods=["POST"])
def register():
    post_data = request.json
    user_name = post_data["user"]
    user_password = post_data["password"]
    return user_service.create_user(user_name, user_password)


@app.route("/login/", methods=["POST"])
def login():
    post_data = request.json
    user_name = post_data["user"]
    user_password = post_data["password"]
    return user_service.login(user_name, user_password)


@app.route("/todos/", methods=["GET"])
@jwt_required()
def list_todos():
    return todo_service.get_all_todo()


@app.route("/todos/", methods=["POST"])
@jwt_required()
def add_todo():
    post_data = request.json
    title = post_data["title"]
    description = post_data["description"]
    status = post_data["status"]
    do_time = post_data["do_time"]
    return todo_service.add_single_todo(title, description, status, do_time)


@app.route("/todos/<task_id>", methods=["GET"])
@jwt_required()
def get_single_task(task_id):
    return todo_service.get_single_todo(task_id)


@app.route("/todos/<task_id>", methods=["DELETE"])
@jwt_required()
def delete_single_task(task_id):
    return todo_service.delete_single_todo(task_id)


@app.route("/todos/<task_id>", methods=["PUT"])
@jwt_required()
def update_single_task(task_id):
    post_request = request.json
    return todo_service.update_single_todo(post_request, task_id)


# return all tasks from one user
@app.route("/users/<user_id>/todos/", methods=["GET"])
@jwt_required()
def todos_user(user_id):
    return todo_service.get_user_todos(user_id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

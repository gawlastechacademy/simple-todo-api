import os
from flask import Flask, request, jsonify, make_response
import json_connection as data_connection
from dotenv import load_dotenv

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
    if data_connection.register(user_name, user_password, user_admin):
        return make_response(jsonify({"description": f"User '{user_name}' successfully registered"}), 201)
    else:
        return make_response(jsonify({"description": f"User '{user_name}' already exists in database"}), 409)


@app.route("/login/", methods=["POST"])
def login():
    post_data = request.json
    user_name = post_data["user"]
    user_password = post_data["password"]

    if data_connection.login(user_name, user_password):
        return make_response(jsonify({"description": f"Login successful for user '{user_name}'"}), 200)

    else:
        return make_response(jsonify({"description": "Wrong username or password"}), 400)

#return all task from all users
@app.route("/todos/", methods=["GET", "POST"])
def todos():
    if request.method == "GET":
        if data_connection.see_all_task_all_users() is not None:
            return make_response(jsonify({"description": data_connection.see_all_task_all_users()}), 200)
        else:
            return make_response(jsonify({"description": "Tasks not found"}), 404)
    if request.method == "POST":
        post_data = request.json
        title = post_data["title"]
        description = post_data["description"]
        status = post_data["status"]
        do_time = post_data["do_time"]
        user_id = post_data["user_id"]

        if data_connection.add_task(user_id, title, description, status, do_time):
            return make_response(jsonify({"description": f"Task '{title}' added successfully"}), 201)
        else:
            return make_response(jsonify({"description": "Wrong request"}), 400)

#return one task
@app.route("/todos/<task_id>", methods=["GET", "DELETE", "PUT"])
def todos_task(task_id):
    if request.method == "GET":
        if data_connection.see_one_task(task_id) is not None:
            return make_response(jsonify({"description": data_connection.see_one_task(task_id)}), 200)
        else:
            return make_response(jsonify({"description": f"Task '{task_id}' not found"}), 404)
    if request.method == "DELETE":
        if data_connection.delete_task(task_id):
            return make_response(jsonify({"description": f"Task '{task_id}' deleted successfully"}), 200)
        else:
            return make_response(jsonify({"description": f"Task '{task_id}' not found"}), 404)

    if request.method == "PUT":
        post_data = request.json
        change_attribute = post_data["attribute"]
        change_content = post_data["content"]
        if data_connection.change_task(task_id, change_attribute, change_content):
            return make_response(jsonify({"description": f"Task '{task_id}' updated successfully"}), 200)
        else:
            return make_response(jsonify({"description": "Wrong request"}), 404)

# return all tasks from one user
@app.route("/users/<user_id>/todos/", methods=["GET"])
def todos_user(user_id):

    if data_connection.see_all_task_one_user(user_id) is not None:
        return make_response(jsonify({"description": data_connection.see_all_task_one_user(user_id)}), 200)
    else:
        return make_response(jsonify({"description": f"User or tasks not found"}), 404)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

import os
from flask import Flask, request, jsonify, session
import json_connection as data_connection
from dotenv import load_dotenv
# load .env file to environment
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
print(os.getenv('SECRET_KEY'))


@app.route("/")
def hello_world():
    return jsonify("Home page")


@app.route("/register/", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        post_data = request.json
        user_name = post_data["user"]
        user_password = post_data["password"]
        user_admin = post_data["admin"]
        if data_connection.register(user_name, user_password, user_admin):
            session["user"] = user_name
            return jsonify(f"Hi {user_name} you are added to database")
        else:
            return jsonify(f"Hi {user_name} you are in database, you should login")
    else:
        return jsonify("Register page")


@app.route("/login/", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        post_data = request.json
        user_name = post_data["user"]
        user_password = post_data["password"]
        if data_connection.login(user_name, user_password):
            session["user"] = user_name
            return jsonify(f"Hi {user_name} you are log in")
        else:
            return jsonify("Wrong user or password")

    return jsonify("login page")


@app.route("/todos/",  methods=['GET', 'POST'])
def todos():

    if request.method == "GET":
        return data_connection.see_all_task_all_users()
    else:
        post_data = request.json
        title = post_data["title"]
        description = post_data["description"]
        status = post_data["status"]
        do_time = post_data["do_time"]
        user_id = post_data["user_id"]

        return jsonify(data_connection.add_task(user_id, title, description, status, do_time))


@app.route("/todos/<task_id>", methods=['GET','DELETE', 'PUT'])
def todos_task(task_id):
    if request.method == "GET":
        return data_connection.see_one_task(task_id)
    elif request.method == "DELETE":
        return jsonify(data_connection.delete_task(task_id))

    if request.method == "PUT":
        post_data = request.json
        change_attribute = post_data["attribute"]
        change_content = post_data["content"]
        return jsonify(data_connection.change_task(task_id, change_attribute, change_content))

    else:
        return jsonify("Todos page")



#return all tasks from all users
@app.route("/users/<user_id>/todos/", methods=['GET', 'POST'])
def todos_user(user_id):
    if request.method == "GET":
        return jsonify({"response": data_connection.see_all_task_one_user(user_id)})
    else:
        return jsonify("Todo page")
#return all tasks from 1 user

@app.route("/users/<user_id>/tasks/<task_id>/todos/", methods=['GET', 'POST'])
def todos_user_task(user_id, task_id):
    if request.method == "GET":
        return jsonify(data_connection.see_tasks(user_id, task_id))
        return
    else:
        return jsonify("Todo page")
#return all user information

# @app.route("/delete/<task_id>", methods=["DELETE"])
# def delete(task_id):
#     return data_connection .delete_task(task_id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

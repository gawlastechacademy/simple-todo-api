import sqlite3 as sql
from pathlib import Path
from flask import jsonify, make_response
from datetime import datetime


def user_id_exist(user_id):
    data_file = Path(Path.cwd(), "data", "data_sql.db")
    connection = sql.connect(data_file)
    cursor = connection.cursor()
    statement = "SELECT user_id FROM USERS WHERE user_id = ?"
    cursor.execute(statement, (user_id,))
    matching_user = cursor.fetchall()
    return len(matching_user) != 0


def task_id_exist(task_id):
    data_file = Path(Path.cwd(), "data", "data_sql.db")
    connection = sql.connect(data_file)
    cursor = connection.cursor()
    statement = "SELECT task_id FROM TASKS WHERE task_id = ?;"
    cursor.execute(statement, (task_id,))
    matching_task = cursor.fetchall()
    return len(matching_task) != 0


def status_correct(status=str):
    return status.lower() == "to do" or status.lower() == "in progress" or status.lower() == "done"


def tasks_response_builder(task):
    return {"task_id": task[0], "user_id": task[1], "title": task[2], "description": task[3], "status": task[4],
            "create_date": task[5], "do_date": task[6]}


def get_all_todo():
    data_file = Path(Path.cwd(), "data", "data_sql.db")
    connection = sql.connect(data_file)
    cursor = connection.cursor()
    statement = "SELECT * FROM TASKS"
    cursor.execute(statement)
    matching_tasks = cursor.fetchall()
    tasks = [tasks_response_builder(task) for task in matching_tasks]
    return make_response(jsonify(tasks), 200)


def add_single_todo(user_id, title, description, status, do_date):
    data_file = Path(Path.cwd(), "data", "data_sql.db")
    create_time = datetime.now()

    # client errors
    if not status_correct(status):
        return make_response(jsonify({"description": "Wrong request"}), 400)
    if not user_id_exist(user_id):
        return make_response(jsonify({"description": "User id doesn't exist"}), 404)

    connection = sql.connect(data_file)
    cursor = connection.cursor()
    statement = """
    INSERT INTO TASKS(user_id, title, description, status, create_time, do_date)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor.execute(statement, (user_id, title, description, status, str(create_time), do_date))
    connection.commit()
    cursor.close()
    connection.close()
    return make_response(jsonify({"description": f"Task '{title}' added successfully"}), 201)


def get_single_todo(task_id):
    data_file = Path(Path.cwd(), "data", "data_sql.db")
    connection = sql.connect(data_file)
    cursor = connection.cursor()
    statement = "SELECT * FROM TASKS WHERE task_id = ?"
    cursor.execute(statement, (task_id,))
    task_matching = cursor.fetchall()
    if len(task_matching) == 0:
        return make_response(jsonify({"description": f"task '{task_id}' not found"}), 404)
    else:
        return make_response(
            jsonify(tasks_response_builder(task_matching[0]), 200))


def delete_single_todo(task_id):
    data_file = Path(Path.cwd(), "data", "data_sql.db")
    connection = sql.connect(data_file)
    cursor = connection.cursor()
    # check if task exist
    statement = "SELECT * FROM TASKS WHERE task_id = ?"
    cursor.execute(statement, (task_id,))
    deleted_task = cursor.fetchall()

    if len(deleted_task) == 0:
        return make_response(jsonify({"description": f"Task '{task_id}' not found"}), 404)
    else:
        statement = "DELETE FROM TASKS WHERE task_id = ?"
        cursor.execute(statement, (task_id,))
        connection.commit()
        cursor.close()
        connection.close()
        return make_response(jsonify({"description": f"Task '{task_id}' successfully deleted"}), 200)


def update_single_todo(post_request, task_id):
    mutable_tasks_file = ("title", "description", "status", "do_date")
    change_tasks_file = []
    data_file = Path(Path.cwd(), "data", "data_sql.db")
    status_in_request = "status" in post_request.keys()

    if not task_id_exist(task_id):
        return make_response(jsonify({"description": f"Task id '{task_id}' doesn't exist"}), 404)

    if status_in_request:
        if not status_correct(post_request["status"]):
            return make_response(jsonify({"description": "Wrong request, status doesn't exist"}), 404)

    # check if request keys are correct
    for key in post_request:
        if key in mutable_tasks_file:
            change_tasks_file.append(key)

    connection = sql.connect(data_file)
    cursor = connection.cursor()

    # change in database
    for file in change_tasks_file:
        statement = f"UPDATE TASKS SET {file} = ? WHERE task_id = ?"
        cursor.execute(statement, (post_request[file], task_id))
        connection.commit()
    cursor.close()
    connection.close()
    return make_response(jsonify({"description": f"Task '{task_id}' updated successfully"}), 200)


def get_user_todos(user_id):
    data_file = Path(Path.cwd(), "data", "data_sql.db")
    connection = sql.connect(data_file)
    cursor = connection.cursor()
    statement = "SELECT * FROM TASKS WHERE user_id = ?"
    cursor.execute(statement, (user_id,))
    matching_tasks = cursor.fetchall()
    tasks = [tasks_response_builder(task) for task in matching_tasks]
    if len(matching_tasks) == 0:
        return make_response(jsonify({"description": "Wrong user id"}), 404)
    return make_response(jsonify(tasks), 200)


if __name__ == '__main__':
    pass
    # test_request = {"title": "test title", "status": "done"}
    # update_single_todo(test_request, 2)
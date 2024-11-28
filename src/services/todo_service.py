import sqlite3 as sql
from pathlib import Path
from flask import jsonify, make_response
from datetime import datetime


def user_id_exist(data_file, user_id):
    connection = sql.connect(data_file)
    cursor = connection.cursor()

    statement = """
    SELECT user_id
    FROM USERS
    WHERE user_id = ?;
    """
    cursor.execute(statement, (user_id,))
    sql_file = cursor.fetchall()

    return bool(sql_file)


def get_all_todo():
    data_file = Path(Path.cwd(), "data", "data_sql.db")
    connection = sql.connect(data_file)
    cursor = connection.cursor()

    statement = "SELECT * FROM TASKS"
    cursor.execute(statement)
    sql_data = cursor.fetchall()

    return make_response(jsonify(sql_data), 200)


def add_single_todo(user_id, title, description, status, do_date):
    data_file = Path(Path.cwd(), "data", "data_sql.db")
    create_time = datetime.now()

    if status.lower() == "to do" or status.lower() == "in progress" or status.lower() == "done":
        if user_id_exist(data_file, user_id):
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
        else:
            return make_response(jsonify({"description": "User id doesn't exist"}), 404)
    else:
        return make_response(jsonify({"description": "Wrong request"}), 400)


def get_single_todo(task_id):
    data_file = Path(Path.cwd(), "data", "data_sql.db")

    connection = sql.connect(data_file)
    cursor = connection.cursor()
    statement = "SELECT * FROM TASKS WHERE task_id = ?"
    cursor.execute(statement, (task_id,))
    sql_data = cursor.fetchall()

    if len(sql_data) == 0:
        return make_response(jsonify({"description": f"task '{task_id}' not found"}), 404)

    return make_response(jsonify(id=sql_data[0][0]), 200)


def delete_single_todo():
    data_file = Path(Path.cwd(), "data", "data_sql.db")
    pass


def update_single_todo():
    data_file = Path(Path.cwd(), "data", "data_sql.db")
    pass


def get_user_todos():
    data_file = Path(Path.cwd(), "data", "data_sql.db")
    pass


if __name__ == '__main__':
    get_single_todo("1")

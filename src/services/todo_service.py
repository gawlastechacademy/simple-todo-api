import sqlite3 as sql
from pathlib import Path
from flask import jsonify, make_response
from datetime import datetime


def user_id_exist(data_file, user_id):
    connection = sql.connect(data_file)
    cursor = connection.cursor()
    statement = "SELECT user_id FROM USERS WHERE user_id = ?;"
    cursor.execute(statement, (user_id,))
    sql_file = cursor.fetchall()
    return bool(sql_file)


def task_id_exist(data_file, task_id):
    connection = sql.connect(data_file)
    cursor = connection.cursor()
    statement = " SELECT task_id FROM TASKS WHERE task_id = ?;"
    cursor.execute(statement, (task_id,))
    sql_file = cursor.fetchall()
    if len(sql_file) == 0:
        return False
    return True


def get_all_todo():
    data_file = Path(Path.cwd(), "data", "data_sql.db")
    connection = sql.connect(data_file)
    cursor = connection.cursor()

    statement = "SELECT * FROM TASKS"
    cursor.execute(statement)
    sql_data = cursor.fetchall()
    tasks = [{"task_id": task[0], "user_id": task[1], "title": task[2], "description": task[3], "status": task[4],
              "create_date": task[5], "do_date": task[6]} for task in sql_data]
    return make_response(jsonify(tasks), 200)


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
    return make_response(
        jsonify(task_id=sql_data[0][0], user_id=sql_data[0][1], title=sql_data[0][2], description=sql_data[0][3],
                status=sql_data[0][4], create_date=sql_data[0][5], do_date=sql_data[0][6]), 200)


def delete_single_todo(task_id):
    data_file = Path(Path.cwd(), "data", "data_sql.db")
    connection = sql.connect(data_file)
    cursor = connection.cursor()
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
        return make_response(jsonify({"description": f"Task '{task_id}' deleted successfully"}), 200)


def update_single_todo(task_id, change_attribute, change_content):
    data_file = Path(Path.cwd(), "data", "data_sql.db")
    connection = sql.connect(data_file)
    cursor = connection.cursor()
    if task_id_exist(data_file, task_id):
        if change_attribute.lower() == "title":
            statement = "UPDATE TASKS SET title = ? WHERE task_id = ?"
            cursor.execute(statement, (change_content, task_id))
            connection.commit()
            cursor.close()
            connection.close()
            return make_response(jsonify({"description": f"Task '{task_id}' updated successfully"}), 200)
        elif change_attribute.lower() == "description":
            statement = "UPDATE TASKS SET description = ? WHERE task_id = ?"
            cursor.execute(statement, (change_content, task_id))
            connection.commit()
            cursor.close()
            connection.close()
            return make_response(jsonify({"description": f"Task '{task_id}' updated successfully"}), 200)
        elif change_attribute.lower() == "status":
            if change_content.lower() == "to do" or change_content.lower() == "in progress" or change_content.lower() == "done":
                statement = "UPDATE TASKS SET status = ? WHERE task_id = ?"
                cursor.execute(statement, (change_content.lower(), task_id))
                connection.commit()
                cursor.close()
                connection.close()
                return make_response(jsonify({"description": f"Task '{task_id}' updated successfully"}), 200)
            else:
                return make_response(jsonify({"description": "Wrong request"}), 404)
        elif change_attribute.lower() == "do_date":
            statement = "UPDATE TASKS SET do_date = ? WHERE task_id = ?"
            cursor.execute(statement, (change_content, task_id))
            connection.commit()
            cursor.close()
            connection.close()
            return make_response(jsonify({"description": f"Task '{task_id}' updated successfully"}), 200)
        else:
            return make_response(jsonify({"description": "Wrong request"}), 404)
    else:
        return make_response(jsonify({"description": "Wrong request"}), 404)


def get_user_todos(user_id):
    data_file = Path(Path.cwd(), "data", "data_sql.db")
    connection = sql.connect(data_file)
    cursor = connection.cursor()
    statement = "SELECT * FROM TASKS WHERE user_id = ?"
    cursor.execute(statement, (user_id,))
    sql_data = cursor.fetchall()
    tasks = [{"task_id": task[0], "user_id": task[1], "title": task[2], "description": task[3], "status": task[4],
              "create_date": task[5], "do_date": task[6]} for task in sql_data]
    if len(sql_data) == 0:
        return make_response(jsonify({"description": "Wrong user id"}), 404)
    else:
        return make_response(jsonify(tasks), 200)


if __name__ == '__main__':
    get_single_todo("1")

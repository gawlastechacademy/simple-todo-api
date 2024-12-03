import sqlite3 as sql
from pathlib import Path
from flask import jsonify, make_response


def user_exist(data_file, user):
    connection = sql.connect(data_file)
    cursor = connection.cursor()
    statement = "SELECT user_id FROM USERS WHERE user_name = ?;"
    cursor.execute(statement, (user,))
    matching_user = cursor.fetchall()
    return len(matching_user) != 0


def create_user(user, password, admin="False"):
    data_file = Path(Path.cwd(), "data", "data_sql.db")
    connection = sql.connect(data_file)
    cursor = connection.cursor()
    # client errors
    if user_exist(data_file, user):
        return make_response(jsonify({"description": f"User '{user}' already exists in database"}), 409)
    else:
        statement = "INSERT INTO USERS (user_name, user_password, admin) VALUES (?,?,?);"
        cursor.execute(statement, (user, password, admin))
        connection.commit()
        cursor.close()
        connection.close()
        return make_response(jsonify({"description": f"User '{user}' successfully registered"}), 201)


def login(user, password):
    data_file = Path(Path.cwd(), "data", "data_sql.db")
    connection = sql.connect(data_file)
    cursor = connection.cursor()
    statement = "SELECT user_id, user_name FROM USERS WHERE user_name = ? AND user_password = ?;"
    cursor.execute(statement, (user, password))
    sql_file = cursor.fetchall()
    # client errors
    if len(sql_file) == 0:
        return make_response(jsonify({"description": "Wrong username or password"}), 400)
    else:
        return make_response(jsonify({"description": f"Login successful for user '{user}'"}), 200)

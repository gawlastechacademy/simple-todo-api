import sqlite3 as sql
from pathlib import Path


def check_and_create_db():
    checked_directory = Path(Path.cwd(), "data")
    checked_file = Path(Path.cwd(), "data", "data_sql.db")

    if Path.exists(checked_directory):
        if Path.exists(checked_file):
            return checked_file
        else:
            connection = sql.connect(checked_file)
            cursor = connection.cursor()
            statement = """
                CREATE TABLE USERS (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name TEXT NOT NULL,
                    user_password TEXT NOT NULL,
                    admin TEXT NOT NULL
                    );
                """
            cursor.execute(statement)
            connection.commit()
            cursor.close()
            connection.close()

            connection = sql.connect(checked_file)
            cursor = connection.cursor()
            statement = """
                CREATE TABLE TASKS (
                    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    status TEXT NOT NULL,
                    create_time TEXT NOT NULL,
                    do_date TEXT NULL
                    );
                """
            cursor.execute(statement)
            connection.commit()

            cursor.close()
            connection.close()
            return checked_file

    else:
        Path.mkdir("data")
        connection = sql.connect(checked_file)
        cursor = connection.cursor()
        statement = """
                CREATE TABLE USERS (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name TEXT NOT NULL,
                    user_password TEXT NOT NULL,
                    admin TEXT NOT NULL
                    );
                """
        cursor.execute(statement)
        connection.commit()
        statement = """
                CREATE TABLE TASKS (
                    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    status TEXT NOT NULL,
                    create_time TEXT NOT NULL,
                    do_date TEXT NULL
                    );
                """
        cursor.execute(statement)
        connection.commit()

        cursor.close()
        connection.close()
        return checked_file

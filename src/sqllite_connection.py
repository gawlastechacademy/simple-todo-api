import sqlite3 as sql
from pathlib import Path
from datetime import datetime


def check_and_create_data_file():
    checked_directory = Path(Path.cwd(), "data")
    checked_file = Path(Path.cwd(), "data", "data_sql.db")

    if Path.exists(checked_directory):
        if Path.exists(checked_file):
            print("Directory and file exist")
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
                    user_id TEXT NOT NULL,
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
            print("File was created")

            return checked_file

    else:
        Path.mkdir("data")
        connection = sql.connect(checked_file)
        cursor = connection.cursor()
        statement = """
                CREATE TABLE USERS (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name TEXT NOT NULL,
                    last_password TEXT NOT NULL
                    );
                """
        cursor.execute(statement)
        connection.commit()
        statement = """
                CREATE TABLE TASKS (
                    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
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
        print("File was created")
        return checked_file


def check_admin(user):
    checked_file = check_and_create_data_file()
    connection = sql.connect(checked_file)
    cursor = connection.cursor()
    statement = """
    SELECT admin
    FROM USERS
    WHERE user_name = ?
    """
    cursor.execute(statement, (user,))
    sql_file = cursor.fetchone()
    print(sql_file[0])
    return sql_file[0]


def user_exist(data_file, user):
    connection = sql.connect(data_file)
    cursor = connection.cursor()

    statement = """
    SELECT user_id
    FROM USERS
    WHERE user_name = ?;
    """
    cursor.execute(statement, (user,))
    sql_file = cursor.fetchall()

    if bool(sql_file):
        return True
    return False


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

def task_id_exist(data_file, task_id):
    connection = sql.connect(data_file)
    cursor = connection.cursor()

    statement = """
    SELECT task_id
    FROM TASKS
    WHERE task_id = ?;
    """
    cursor.execute(statement, (task_id,))
    sql_file = cursor.fetchall()

    return bool(sql_file)


def register(user, password, admin="False"):
    data_file = check_and_create_data_file()
    connection = sql.connect(data_file)
    cursor = connection.cursor()

    if user_exist(data_file, user):
        print("user exist, choose different name")
        return False
    else:
        statement = """
        INSERT INTO USERS (user_name, user_password, admin)
        VALUES (?,?,?);
        """
        cursor.execute(statement, (user, password, admin))
        connection.commit()
        cursor.close()
        connection.close()


def login(user, password):
    data_file = check_and_create_data_file()
    connection = sql.connect(data_file)
    cursor = connection.cursor()
    statement = """
    SELECT user_id, user_name 
    FROM USERS
    WHERE user_name = ? AND user_password = ?;
    """
    cursor.execute(statement, (user, password))
    sql_file = cursor.fetchall()

    if bool(sql_file):
        print("You are login")
        return True
    print("wrong user or password")
    return False


def add_task(user_id, title, description, status, do_date):
    data_file = check_and_create_data_file()
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

            return {"response": "New task was added"}
        else:
            print(f"You can't add task because user ID {user_id} doesn't exist")
            return {"response": f"You can't add task because user ID {user_id} doesn't exist"}
    else:
        print(f"Status '{status}' doesn't exist")
        return f"Status '{status}' doesn't exist"

def see_all_task_all_users():
    data_file = check_and_create_data_file()
    connection = sql.connect(data_file)
    cursor = connection.cursor()


    statement = """
    SELECT * FROM TASKS
    """
    cursor.execute(statement)
    sql_data = cursor.fetchall()

    return sql_data


def see_all_task_one_user(user_id):
    data_file = check_and_create_data_file()
    connection = sql.connect(data_file)
    cursor = connection.cursor()
    statement = """
    SELECT * FROM TASKS
    WHERE user_id = ?
    """
    cursor.execute(statement, (user_id,))
    sql_data = cursor.fetchall()

    if bool(sql_data):
        return sql_data
    else:
        print(f"User id {user_id} doesn't exist")
        return f"User id {user_id} doesn't exist"



def see_one_task(task_id):
    data_file = check_and_create_data_file()
    connection = sql.connect(data_file)
    cursor = connection.cursor()
    statement = """
    SELECT * FROM TASKS
    WHERE task_id = ?
    """
    cursor.execute(statement, (task_id,))
    sql_data = cursor.fetchall()
    print(bool(sql_data))
    if bool(sql_data):
        return sql_data
    else:
        print(f"Task {task_id} doesn't exist")
        return f"Task {task_id} doesn't exist"


def see_all_tasks_all_users():
    data_file = check_and_create_data_file()
    connection = sql.connect(data_file)
    cursor = connection.cursor()
    statement = """
    SELECT * FROM TASKS
    """
    cursor.execute(statement)
    sql_all_tasks = cursor.fetchall()

    print(sql_all_tasks)
    return sql_all_tasks


def change_task(task_id, change_attribute, change_content):
    data_file = check_and_create_data_file()
    connection = sql.connect(data_file)
    cursor = connection.cursor()

    if task_id_exist(data_file, task_id):

        if change_attribute.lower() == "title":
            statement = """
            UPDATE TASKS
            SET title = ?
            WHERE task_id = ?
            """
            cursor.execute(statement, (change_content, task_id))
            connection.commit()
            cursor.close()
            connection.close()
            print(f"Change '{change_attribute}' to '{change_content}' in '{task_id}' task.")
            return f"Change '{change_attribute}' to '{change_content}' in '{task_id}' task."

        elif change_attribute.lower() == "description":
            statement = """
            UPDATE TASKS
            SET description = ?
            WHERE task_id = ?
            """
            cursor.execute(statement, (change_content, task_id))
            connection.commit()
            cursor.close()
            connection.close()
            print(f"Change '{change_attribute}' to '{change_content}' in '{task_id}' task.")
            return f"Change '{change_attribute}' to '{change_content}' in '{task_id}' task."

        elif change_attribute.lower() == "status":

            if change_content.lower() == "to do" or change_content.lower() == "in progress" or change_content.lower() == "done":
                statement = """
                UPDATE TASKS
                SET status = ?
                WHERE task_id = ?
                """
                cursor.execute(statement, (change_content.lower(), task_id))
                connection.commit()
                cursor.close()
                connection.close()
                print(f"Change '{change_attribute}' to '{change_content.lower()}' in '{task_id}' task.")
                return f"Change '{change_attribute}' to '{change_content.lower()}' in '{task_id}' task."
            else:
                print(f"Status '{change_content}' doesn't exist")
                return f"Status '{change_content}' doesn't exist"

        elif change_attribute.lower() == "do_date":
            statement = """
            UPDATE TASKS
            SET do_date = ?
            WHERE task_id = ?
            """
            cursor.execute(statement, (change_content, task_id))
            connection.commit()
            cursor.close()
            connection.close()
            print(f"Change '{change_attribute}' to '{change_content}' in '{task_id}' task.")
            return f"Change '{change_attribute}' to '{change_content}' in '{task_id}' task."

        else:
            print(f"This '{change_attribute}' doesn't exist.")
            return f"This '{change_attribute}' doesn't exist."
    else:
        print(f"Task {task_id} doesn't exist")
        return f"Task {task_id} doesn't exist"



def delete_task(task_id):
    data_file = check_and_create_data_file()
    connection = sql.connect(data_file)
    cursor = connection.cursor()

    statement = """
    SELECT * FROM TASKS
    WHERE task_id = ?
    """
    cursor.execute(statement, (task_id,))
    deleted_task = cursor.fetchall()

    if bool(deleted_task):
        statement = """
        DELETE FROM TASKS
        WHERE task_id = ?
        """
        cursor.execute(statement, (task_id,))

        connection.commit()
        cursor.close()
        connection.close()
        return f"task {task_id} was deleted"
    else:
        print(f"task {task_id} doesn't exist in database")
        return f"task {task_id} doesn't exist in database"


if __name__ == '__main__':
    # register("aga", "test123", "False")
    add_task("222", "love", "work work work", "in progress", "20-11-2024")
    # change_task("3", "status", "change description 3")
    # see_one_task("33")
    # delete_task("111")

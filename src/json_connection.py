import json
from pathlib import Path
from datetime import datetime


def check_and_create_data_file_users():
    checked_directory = Path(Path.cwd(), "data")
    checked_file = Path(Path.cwd(), "data", "user_data.json")

    if Path.exists(checked_directory):
        if Path.exists(checked_file):
            print("Directory and file users exist")
            return checked_file
        else:
            with open(checked_file, "w") as file:
                setup_data = {}
                json.dump(setup_data, file)
                file.close()
                print("File was created")
                return checked_file

    else:
        Path.mkdir("data")
        with open(checked_file, "w") as file:
            setup_data = {}
            json.dump(setup_data, file)
            print("File and data was created")
            return checked_file


def next_user_id(json_file):
    with open(json_file, "r+") as file:
        json_data = json.load(file)
        if bool(json_data):
            return max(list(int(num) for num in json_data.keys())) + 1
        else:
            return 0


def next_task_id(json_file):
    with open(json_file, "r+") as file:
        json_data = json.load(file)
        if bool(json_data):
            return max(list(int(num) for num in json_data.keys())) + 1
        else:
            return 0


def check_and_create_data_file_tasks():
    checked_directory = Path(Path.cwd(), "data")
    checked_file = Path(Path.cwd(), "data", "task_data.json")

    if Path.exists(checked_directory):
        if Path.exists(checked_file):
            print("Directory and file tasks exist")
            return checked_file
        else:
            with open(checked_file, "w") as file:
                setup_data = {}
                json.dump(setup_data, file)
                file.close()
                print("File was created")
                return checked_file

    else:
        Path.mkdir("data")
        with open(checked_file, "w") as file:
            setup_data = {}
            json.dump(setup_data, file)
            print("File and data was created")
            return checked_file


def check_user(user, json_data):
    if bool(json_data):
        for key, value in json_data.items():
            if value["user"] == user:
                return key
        return False


def check_task_id(task_id, json_data):
    if bool(json_data):
        for key, value in json_data.items():
            if key == task_id:
                return True
    else:
        return False


def check_admin(user):
    json_file = check_and_create_data_file_users()
    with open(json_file, "r+") as file:
        json_data = json.load(file)
        user_id = check_user(user, json_data)
        print(f"user id {user_id}")
        print(json_data[user_id]["admin"])
        return json_data[user_id]["admin"]


def check_password(user, password, json_data):
    if bool(json_data):
        for key, value in json_data.items():
            if value["user"] == user and value["password"] == password:
                return True
        return False


def register(user, password, admin="False"):
    json_file = check_and_create_data_file_users()
    user_id = next_user_id(json_file)
    with open(json_file, "r+") as file:
        json_data = json.load(file)
        if bool(check_user(user, json_data)):
            print("User exist in data base")
            return False
        else:
            new_user_json = {str(user_id): {"id": str(user_id), "user": user, "password": password, "admin": admin}}
            json_data.update(new_user_json)
            with open(json_file, "w") as file:
                file.seek(0)
                json.dump(json_data, file, indent=6)
                print("User added to database")
                return True


def login(user, password):
    json_file = check_and_create_data_file_users()
    with open(json_file, "r+") as file:
        json_data = json.load(file)
        if check_password(user, password, json_data):
            return True
    return False


def add_task(user_id, title, description, status, do_time):
    if status.lower() == "to do" or status.lower() == "in progress" or status.lower() == "done":
        json_file = check_and_create_data_file_tasks()
        users_file = check_and_create_data_file_users()
        task_id = next_task_id(json_file)
        task_date_time = datetime.now()

        with open(json_file, "r+") as file:
            json_data = json.load(file)
            with open(users_file, "r+") as file_users:
                json_users_data = json.load(file_users)
                if user_id in json_users_data.keys():
                    new_task_json = {
                        str(task_id): {"user_id": user_id, "task_id": str(task_id), "task_title": title,
                                       "task_description": description, "task_status": status,
                                       "create_time": str(task_date_time), "do_time": do_time, }}
                    json_data.update(new_task_json)
                    with open(json_file, "w") as file:
                        file.seek(0)
                        json.dump(json_data, file, indent=6)
                        return {"response": "New task was added"}
                else:
                    return {"response": "You can't add task because user ID doesn't exist"}
    else:
        print(f"Status '{status}' doesn't exist")
        return f"Status '{status}' doesn't exist"

def see_all_task_all_users():
    json_file = check_and_create_data_file_tasks()
    with open(json_file, "r+") as file:
        json_data = json.load(file)
        return json_data


def see_all_task_one_user(user_id):
    json_file = check_and_create_data_file_tasks()
    with open(json_file, "r+") as file:
        json_data = json.load(file)
        selected_file = {}
        for key, value in json_data.items():
            if value["user_id"] == user_id:
                selected_file[key] = value
        if bool(selected_file):
            return selected_file
        else:
            print(f"User id {user_id} doesn't exist")
            return f"User id {user_id} doesn't exist"


def see_one_task(task_id):
    json_file = check_and_create_data_file_tasks()
    with open(json_file, "r+") as file:
        json_data = json.load(file)
        selected_file = {}
        for key, value in json_data.items():
            if key == task_id:
                selected_file[key] = value
        if bool(selected_file):
            return selected_file
        print(f"Task {task_id} doesn't exist")
        return f"Task {task_id} doesn't exist"

def change_task(task_id, change_attribute, change_content):
    data_file = check_and_create_data_file_tasks()
    with open(data_file, "+r") as file:
        json_data = json.load(file)
        if check_task_id(task_id, json_data):
            if change_attribute == "title":
                json_data[task_id]["task_title"] = change_content
                with open(data_file, "w") as file:
                    file.seek(0)
                    json.dump(json_data, file, indent=6)

                    print(f"Change '{change_attribute}' to '{change_content}' in '{task_id}' task.")
                    return f"Change '{change_attribute}' to '{change_content}' in '{task_id}' task."

            if change_attribute == "description":
                json_data[task_id]["task_description"] = change_content

                with open(data_file, "w") as file:
                    file.seek(0)
                    json.dump(json_data, file, indent=6)

                    print(f"Change '{change_attribute}' to '{change_content}' in '{task_id}' task.")
                    return f"Change '{change_attribute}' to '{change_content}' in '{task_id}' task."

            if change_attribute == "status":
                if change_content.lower() == "to do" or change_content.lower() == "in progress" or change_content.lower() == "done":
                    json_data[task_id]["task_status"] = change_content

                    with open(data_file, "w") as file:
                        file.seek(0)
                        json.dump(json_data, file, indent=6)

                        print(f"Change '{change_attribute}' to '{change_content}' in '{task_id}' task.")
                        return f"Change '{change_attribute}' to '{change_content}' in '{task_id}' task."
                else:
                    print(f"Status '{change_content}' doesn't exist")
                    return f"Status '{change_content}' doesn't exist"

            if change_attribute == "do_date":
                json_data[task_id]["do_time"] = change_content

                with open(data_file, "w") as file:
                    file.seek(0)
                    json.dump(json_data, file, indent=6)

                    print(f"Change '{change_attribute}' to '{change_content}' in '{task_id}' task.")
                    return f"Change '{change_attribute}' to '{change_content}' in '{task_id}' task."
            else:
                print(f"This '{change_attribute}' doesn't exist.")
                return f"This '{change_attribute}' doesn't exist."
        else:
            print(f"Task '{task_id}' doesn't exist.")
            return f"Task '{task_id}' doesn't exist."


def delete_task(task_id):
    json_file = check_and_create_data_file_tasks()
    with open(json_file, "r+") as file:
        json_data = json.load(file)
        if task_id in json_data.keys():
            json_data.pop(task_id)
            with open(json_file, "w") as file:
                json.dump(json_data, file, indent=6)
                return {"response": f"{task_id} was deleted"}
        return {"response": f"{task_id} doesn't exist"}


if __name__ == '__main__':
    change_task("3", "status", "todo")

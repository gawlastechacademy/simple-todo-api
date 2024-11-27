# simple-todo-api
REST API for simple todo application

## DESCRIPTION
Simple task management, this is application building with Python and Flask framework. 
The application helps to create task, show all task, show selected task and delete selected task. 
Data is sent in Json file. 

Command:

POST - add task
GET - show all tasks
GET + ID - show selected task with specific IT 
DELETE + ID - delete selected task

## How to Set Up Project

create virtual env

`python -m venv .venv`

activate virtual env

```
# windows (cmd)
.\.venv\Scripts\activate.bat

# windows (PowerShell)
.\.venv\Scripts\activate.ps1

# macos, linux
source .venv/bin/activate
```

install project dependencies

`pip install .`

## How to run server

you can start flask application by several different way:

run as python script

`python src/01_flask_simple/app.py`

run with flask

`python -m flask --app src/app/app.py run --host 0.0.0.0 --port 8080`

run with flask (with debug & autoreload)

`python -m flask --app src/app/app.py --debug run --host 0.0.0.0 --port 8080`

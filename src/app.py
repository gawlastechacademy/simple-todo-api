from flask import Flask
from src.database import db
from flask_jwt_extended import JWTManager
from src.routes.todo_route import todo_app
from src.routes.user_route import user_app

app = Flask(__name__)
app.register_blueprint(todo_app)
app.register_blueprint(user_app)

app.config.from_object("config.Config")
db.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

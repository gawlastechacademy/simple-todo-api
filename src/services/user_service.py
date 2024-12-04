from flask import jsonify
from src.database import db
from src.models.user import User


def create_user(user_name, password, admin="False"):
    user = User.query.filter(User.user_name == user_name).first()

    if user is not None:
        return jsonify({"description": f"user '{user_name}' already exists in database"}), 409

    new_user = User(
        user_name=user_name,
        user_password=password,
        admin=admin
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201


def login(user_name, password):
    user = User.query.filter(User.user_name == user_name and User.user_password == password).first()

    if user is None:
        return jsonify({"description": "wrong username or password"}), 400

    return jsonify({"description": f"login successful for user '{user.user_name}'"}), 200

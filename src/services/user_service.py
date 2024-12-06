from flask import jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity

from src.database import db
from src.models.user import User


def create_user(user_name, password):
    user = User.query.filter(User.user_name == user_name).first()

    if user is not None:
        return jsonify({"description": f"user '{user_name}' already exists in database"}), 409

    new_user = User(
        user_name=user_name,
        user_password=password,
        is_admin=False
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201


def login(user_name, password):
    user = User.query.filter(User.user_name == user_name and User.user_password == password).first()

    if user is None:
        return jsonify({"description": "wrong username or password"}), 400

    access_token = create_access_token(identity=user_name)
    return jsonify(access_token=access_token), 200


def get_current_user():
    current_user = get_jwt_identity()
    user = User.query.filter(User.user_name == current_user).first()

    return user


def is_admin():
    current_user = get_jwt_identity()
    user = User.query.filter(User.user_name == current_user).first()
    return user.is_admin == 1

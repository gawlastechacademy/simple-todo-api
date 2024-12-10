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


def get_all_users():
    user = get_current_user()
    if not user.is_administrator():
        return jsonify({"description": "unauthorized"}), 401
    users = User.query.all()
    user_dict = [user.to_dict() for user in users]
    return jsonify(user_dict), 200


def get_single_user(user_id):
    user_logged = get_current_user()
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"description": f"user '{user_id}' not found"}), 404

    if user.user_id != user_logged.user_id and not user_logged.is_administrator():
        return jsonify({"description": "Unauthorized"}), 401

    return jsonify(user.to_dict()), 200


def delete_single_user(user_id):
    user = User.query.get(user_id)
    user_logged = get_current_user()

    if user is None:
        return jsonify({"description": f"user '{user_id}' not found"}), 404

    if user.user_id != user_logged.user_id and not user_logged.is_administrator():
        return jsonify({"description": "unauthorized"}), 401

    db.session.delete(user)
    db.session.commit()

    return jsonify({"description": "user deleted"}), 200


def change_single_user(data, user_id):
    pass
    user = User.query.get(user_id)
    user_logged = get_current_user()

    # check errors
    if user is None:
        return jsonify({"description": f"user '{user_id}' not found"}), 404

    if not user_logged.is_administrator():
        return jsonify({"description": "unauthorized"}), 401

    # update user fields
    if "is_admin" in data.keys():
        user.is_admin = data["is_admin"]

    db.session.commit()

    return jsonify(user.to_dict()), 200

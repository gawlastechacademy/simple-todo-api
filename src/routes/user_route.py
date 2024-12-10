from flask import Blueprint, request
import src.services.user_service as user_service
from flask_jwt_extended import jwt_required

user_app = Blueprint("user", __name__)


@user_app.route("/register/", methods=["POST"])
def register():
    post_data = request.json
    user_name = post_data["user"]
    user_password = post_data["password"]
    return user_service.create_user(user_name, user_password)


@user_app.route("/login/", methods=["POST"])
def login():
    post_data = request.json
    user_name = post_data["user"]
    user_password = post_data["password"]
    return user_service.login(user_name, user_password)


@user_app.route("/users/", methods=["GET"])
@jwt_required()
def all_users():
    return user_service.get_all_users()


@user_app.route("/users/<user_id>", methods=["GET"])
@jwt_required()
def single_user(user_id):
    return user_service.get_single_user(user_id)


@user_app.route("/users/<user_id>", methods=["PUT"])
@jwt_required()
def change_user(user_id):
    post_request = request.json
    return user_service.change_single_user(post_request, user_id)


@user_app.route("/users/<user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    return user_service.delete_single_user(user_id)

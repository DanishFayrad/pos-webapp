from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.user_service import (
    create_user_service,
    get_users_service,
    update_user_service
)

user_bp = Blueprint("users", __name__)


@user_bp.route("/users", methods=["POST"])
@jwt_required()
def create_user():
    current_user = get_jwt_identity()
    data = request.get_json()

    response, status = create_user_service(data, current_user)
    return jsonify(response), status


@user_bp.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    current_user = get_jwt_identity()

    response, status = get_users_service(current_user)
    return jsonify(response), status


@user_bp.route("/users/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_user(user_id):
    current_user = get_jwt_identity()
    data = request.get_json()

    response, status = update_user_service(user_id, data, current_user)
    return jsonify(response), status
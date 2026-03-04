from flask import Blueprint, request, jsonify
from services.auth_service import login_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    result, error = login_user(username, password)

    if error:
        return jsonify({"error": error}), 401

    # ✅ Fixed key name
    return jsonify({
        "message": "Login successful",
        "access_token": result["access_token"],
        "role": result["role"],
        "branch_id": result["branch_id"]
    })
from werkzeug.security import generate_password_hash
from repositories.user_repository import (
    create_user,
    get_users_by_branch,
    update_user
)

# ✅ CREATE USER
def create_user_service(data, current_user):

    # Only admin can create
    if current_user["role"] != "admin":
        return {"error": "Only admin can create users"}, 403

    hashed_password = generate_password_hash(data["password"])

    user_id = create_user(
        data["branch_id"],
        data["role"],
        data["full_name"],
        data["username"],
        data.get("email"),
        hashed_password
    )

    return {"message": "User created", "user_id": user_id}, 201


# ✅ GET USERS
def get_users_service(current_user):

    is_admin = current_user["role"] == "admin"
    users = get_users_by_branch(current_user["branch_id"], is_admin)

    result = [
        {
            "user_id": u[0],
            "branch_id": u[1],
            "full_name": u[2],
            "role": u[3],
            "username": u[4],
            "email": u[5],
        }
        for u in users
    ]

    return result, 200


# ✅ UPDATE USER
def update_user_service(user_id, data, current_user):

    if current_user["role"] != "admin":
        return {"error": "Only admin can update users"}, 403

    update_user(user_id, data["full_name"], data["role"])

    return {"message": "User updated"}, 200
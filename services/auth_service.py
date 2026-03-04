from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from repositories.user_repository import find_user_by_username


def login_user(username, password):

    user = find_user_by_username(username)

    if not user:
        return None, "User not found"

    user_id = user[0]
    branch_id = user[1]
    full_name = user[2]
    role = user[3]
    username = user[4]
    stored_password = user[6]

    # ✅ CORRECT HASH CHECK
    if not check_password_hash(stored_password, password):
        return None, "Invalid password"

    token = create_access_token(identity={
        "user_id": user_id,
        "username": username,
        "role": role,
        "branch_id": branch_id
    })

    return {
        "access_token": token,
        "role": role,
        "branch_id": branch_id
    }, None
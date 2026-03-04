from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask import jsonify

def branch_required(fn):

    @wraps(fn)
    def decorator(*args, **kwargs):

        verify_jwt_in_request()

        user = get_jwt_identity()

        request_branch = kwargs.get("branch_id")

        if request_branch and user["branch_id"] != request_branch:
            return jsonify({
                "error": "Branch access denied"
            }), 403

        return fn(*args, **kwargs)

    return decorator
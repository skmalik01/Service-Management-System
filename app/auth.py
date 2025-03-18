from flask import jsonify
from flask_jwt_extended import get_jwt_identity


def role_required(role):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            user = get_jwt_identity()
            if user['role'] != role:
                return jsonify({"error": "Unauthorized Access"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

from flask import jsonify
from flask_jwt_extended import get_jwt
from functools import wraps  

def role_required(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if claims.get("role") != role:
                return jsonify({"error": "Unauthorized Access"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator


from functools import wraps
from flask_jwt_extended import get_jwt_identity
from app.models import User
from app.utils.responses import error

def active_user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = User.query.get(int(get_jwt_identity()))
        if not user or not user.is_active:
            return error("User account is unavailable", 401)
        return fn(*args, **kwargs)
    return wrapper

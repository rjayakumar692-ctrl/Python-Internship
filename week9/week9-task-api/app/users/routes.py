
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import User
from app.utils.responses import success, error
from app.users.schemas import user_update_errors

users_bp = Blueprint("users", __name__)


@users_bp.get("/me")
@jwt_required()
def get_me():
    user = db.session.get(User, int(get_jwt_identity()))
    return success({"user": user.to_dict()}) if user else error("User not found", 404)


@users_bp.patch("/me")
@jwt_required()
def update_me():
    user = db.session.get(User, int(get_jwt_identity()))
    if not user:
        return error("User not found", 404)

    data = request.get_json(silent=True)
    errors = user_update_errors(data)

    if errors:
        return error("Validation failed", 400, errors)

    if "username" in data:
        user.username = data["username"].strip()

    if "email" in data:
        user.email = data["email"].strip().lower()

    db.session.commit()
    return success({"user": user.to_dict()})


@users_bp.delete("/me")
@jwt_required()
def delete_me():
    user = db.session.get(User, int(get_jwt_identity()))
    if not user:
        return error("User not found", 404)

    db.session.delete(user)
    db.session.commit()
    return success({"message": "Account deleted"})

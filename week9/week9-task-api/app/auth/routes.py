from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from app.extensions import db, limiter
from app.models import User
from app.utils.validators import validate_registration
from app.utils.responses import success, error
from app.auth.utils import token_response

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/register")
@limiter.limit("5 per minute")
def register():
    data = request.get_json(silent=True)
    errors = validate_registration(data)
    if errors:
        return error("Validation failed", 400, errors)
    email = data["email"].strip().lower()
    username = data["username"].strip()
    if User.query.filter((User.email == email) | (User.username == username)).first():
        return error("Username or email already registered", 409)
    user = User(username=username, email=email)
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return token_response(user, 201)

@auth_bp.post("/login")
@limiter.limit("10 per minute")
def login():
    data = request.get_json(silent=True) or {}
    identity = str(data.get("email", "")).strip().lower()
    password = data.get("password", "")
    user = User.query.filter_by(email=identity).first()
    if not user or not user.check_password(password) or not user.is_active:
        return error("Invalid email or password", 401)
    return token_response(user)

@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user or not user.is_active:
        return error("User account is unavailable", 401)
    return success({"access_token": create_access_token(identity=str(user.id))})

@auth_bp.post("/password-reset")
@limiter.limit("3 per hour")
def password_reset_request():
    # Demo flow: token is returned only in development. In production, send it by email.
    from flask_jwt_extended import create_access_token
    data = request.get_json(silent=True) or {}
    user = User.query.filter_by(email=str(data.get("email", "")).lower()).first()
    response = {"message": "If the account exists, reset instructions will be sent"}
    if user and current_app.config.get("DEBUG"):
        response["development_reset_token"] = create_access_token(
            identity=str(user.id), additional_claims={"purpose": "password_reset"}
        )
    return success(response)

@auth_bp.post("/password-reset/confirm")
@jwt_required()
def password_reset_confirm():
    from flask_jwt_extended import get_jwt
    claims = get_jwt()
    if claims.get("purpose") != "password_reset":
        return error("A password reset token is required", 403)
    data = request.get_json(silent=True) or {}
    password = data.get("password")
    if not isinstance(password, str) or len(password) < 8:
        return error("Password must contain at least 8 characters", 400)
    user = User.query.get(int(get_jwt_identity()))
    if not user:
        return error("User not found", 404)
    user.set_password(password)
    db.session.commit()
    return success({"message": "Password updated"})

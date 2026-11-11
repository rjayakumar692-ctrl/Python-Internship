from flask import Flask
from dotenv import load_dotenv
from config import Config
from app.extensions import db, migrate, jwt, limiter, cors

def create_app(config_class=Config):
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    limiter.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    from app import models
    from app.auth.routes import auth_bp
    from app.tasks.routes import tasks_bp
    from app.users.routes import users_bp
    from app.utils.responses import register_error_handlers

    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(tasks_bp, url_prefix="/api/v1/tasks")
    app.register_blueprint(users_bp, url_prefix="/api/v1/users")
    register_error_handlers(app)

    @app.get("/health")
    def health():
        return {"status": "ok"}, 200

    @jwt.unauthorized_loader
    def missing_token(reason):
        return {"status": "error", "message": "Authentication required"}, 401

    @jwt.invalid_token_loader
    def invalid_token(reason):
        return {"status": "error", "message": "Invalid token"}, 401

    @jwt.expired_token_loader
    def expired_token(jwt_header, jwt_payload):
        return {"status": "error", "message": "Token has expired"}, 401

    return app

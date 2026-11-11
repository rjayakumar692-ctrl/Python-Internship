from flask import jsonify
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError

def success(data=None, status=200):
    return jsonify({"status": "success", "data": data or {}}), status

def error(message, status=400, errors=None):
    body = {"status": "error", "message": message}
    if errors is not None:
        body["errors"] = errors
    return jsonify(body), status

def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_error(exc):
        return error(exc.description, exc.code or 500)

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(exc):
        from app.extensions import db
        db.session.rollback()
        return error("A record with these details already exists", 409)

    @app.errorhandler(404)
    def not_found(exc):
        return error("Resource not found", 404)

    @app.errorhandler(500)
    def server_error(exc):
        app.logger.exception("Unhandled server error")
        return error("Internal server error", 500)

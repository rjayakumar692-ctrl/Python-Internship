from datetime import date
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_
from app.extensions import db, limiter
from app.models import Task, User, Comment
from app.utils.validators import validate_task
from app.utils.responses import success, error

tasks_bp = Blueprint("tasks", __name__)

def owned_task(task_id, user_id):
    return Task.query.filter_by(id=task_id, user_id=user_id).first()

def parse_task_date(data):
    value = data.get("due_date")
    return date.fromisoformat(value) if value else None

@tasks_bp.get("")
@jwt_required()
def list_tasks():
    user_id = int(get_jwt_identity())
    try:
        page = max(1, request.args.get("page", 1, type=int))
        per_page = request.args.get("per_page", 10, type=int)
        if not 1 <= per_page <= 100:
            return error("per_page must be between 1 and 100", 400)
    except (TypeError, ValueError):
        return error("Invalid pagination values", 400)
    query = Task.query.filter_by(user_id=user_id)
    for field, allowed in (("status", {"pending", "in_progress", "completed"}),
                           ("priority", {"low", "medium", "high"})):
        value = request.args.get(field)
        if value:
            if value not in allowed:
                return error(f"Invalid {field}", 400)
            query = query.filter(getattr(Task, field) == value)
    category = request.args.get("category")
    if category:
        query = query.filter(Task.category == category)
    search = request.args.get("search", "").strip()
    if search:
        term = f"%{search}%"
        query = query.filter(or_(Task.title.ilike(term), Task.description.ilike(term)))
    sort_by = request.args.get("sort_by", "created_at")
    sort_order = request.args.get("sort_order", "desc")
    sortable = {"created_at": Task.created_at, "updated_at": Task.updated_at,
                "due_date": Task.due_date, "priority": Task.priority, "title": Task.title}
    if sort_by not in sortable or sort_order not in {"asc", "desc"}:
        return error("Invalid sorting options", 400)
    column = sortable[sort_by]
    query = query.order_by(column.asc() if sort_order == "asc" else column.desc())
    result = query.paginate(page=page, per_page=per_page, error_out=False)
    return success({"tasks": [t.to_dict() for t in result.items],
                    "pagination": {"page": result.page, "per_page": result.per_page,
                                   "total_pages": result.pages, "total_items": result.total,
                                   "has_next": result.has_next, "has_prev": result.has_prev}})

@tasks_bp.post("")
@jwt_required()
@limiter.limit("30 per minute")
def create_task():
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True)
    errors = validate_task(data)
    if errors:
        return error("Validation failed", 400, errors)
    if data.get("assigned_to_id") and not User.query.get(data["assigned_to_id"]):
        return error("Assignee not found", 404)
    task = Task(title=data["title"].strip(), description=data.get("description", ""),
                status=data.get("status", "pending"), priority=data.get("priority", "medium"),
                category=data.get("category", ""), due_date=parse_task_date(data),
                user_id=user_id, assigned_to_id=data.get("assigned_to_id"))
    db.session.add(task)
    db.session.commit()
    return success({"task": task.to_dict()}, 201)

@tasks_bp.get("/<int:task_id>")
@jwt_required()
def get_task(task_id):
    task = owned_task(task_id, int(get_jwt_identity()))
    if not task:
        return error("Task not found", 404)
    return success({"task": task.to_dict(), "comments": [c.to_dict() for c in task.comments]})

@tasks_bp.route("/<int:task_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_task(task_id):
    task = owned_task(task_id, int(get_jwt_identity()))
    if not task:
        return error("Task not found", 404)
    data = request.get_json(silent=True)
    errors = validate_task(data, partial=request.method == "PATCH")
    if errors:
        return error("Validation failed", 400, errors)
    if request.method == "PUT" and "title" not in data:
        return error("PUT requires title", 400)
    if data.get("assigned_to_id") and not User.query.get(data["assigned_to_id"]):
        return error("Assignee not found", 404)
    for field in ("title", "description", "status", "priority", "category", "assigned_to_id"):
        if field in data:
            value = data[field]
            setattr(task, field, value.strip() if field == "title" else value)
    if "due_date" in data:
        task.due_date = parse_task_date(data)
    db.session.commit()
    return success({"task": task.to_dict()})

@tasks_bp.delete("/<int:task_id>")
@jwt_required()
def delete_task(task_id):
    task = owned_task(task_id, int(get_jwt_identity()))
    if not task:
        return error("Task not found", 404)
    db.session.delete(task)
    db.session.commit()
    return "", 204

@tasks_bp.post("/<int:task_id>/comments")
@jwt_required()
def add_comment(task_id):
    task = owned_task(task_id, int(get_jwt_identity()))
    if not task:
        return error("Task not found", 404)
    data = request.get_json(silent=True) or {}
    body = data.get("body")
    if not isinstance(body, str) or not body.strip() or len(body) > 2000:
        return error("Comment body must contain 1-2000 characters", 400)
    comment = Comment(body=body.strip(), task_id=task.id, user_id=int(get_jwt_identity()))
    db.session.add(comment)
    db.session.commit()
    return success({"comment": comment.to_dict()}, 201)

@tasks_bp.delete("/<int:task_id>/comments/<int:comment_id>")
@jwt_required()
def delete_comment(task_id, comment_id):
    user_id = int(get_jwt_identity())
    task = owned_task(task_id, user_id)
    if not task:
        return error("Task not found", 404)
    comment = Comment.query.filter_by(id=comment_id, task_id=task.id, user_id=user_id).first()
    if not comment:
        return error("Comment not found", 404)
    db.session.delete(comment)
    db.session.commit()
    return "", 204

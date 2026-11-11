from datetime import date
from email_validator import validate_email, EmailNotValidError

STATUSES = {"pending", "in_progress", "completed"}
PRIORITIES = {"low", "medium", "high"}
TASK_FIELDS = {"title", "description", "status", "priority", "category", "due_date", "assigned_to_id"}

def validate_registration(data):
    errors = {}
    if not isinstance(data, dict):
        return {"body": ["A JSON object is required"]}
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    if not isinstance(username, str) or not 3 <= len(username.strip()) <= 40:
        errors["username"] = ["Username must be 3-40 characters"]
    try:
        validate_email(email, check_deliverability=False)
    except (EmailNotValidError, TypeError):
        errors["email"] = ["A valid email address is required"]
    if not isinstance(password, str) or len(password) < 8:
        errors["password"] = ["Password must contain at least 8 characters"]
    return errors

def validate_task(data, partial=False):
    errors = {}
    if not isinstance(data, dict):
        return {"body": ["A JSON object is required"]}
    unknown = set(data) - TASK_FIELDS
    if unknown:
        errors["fields"] = [f"Unknown field(s): {', '.join(sorted(unknown))}"]
    if not partial and not data.get("title"):
        errors["title"] = ["Title is required"]
    if "title" in data and (not isinstance(data["title"], str) or not 3 <= len(data["title"].strip()) <= 160):
        errors["title"] = ["Title must be 3-160 characters"]
    for field, allowed in (("status", STATUSES), ("priority", PRIORITIES)):
        if field in data and data[field] not in allowed:
            errors[field] = [f"Must be one of: {', '.join(sorted(allowed))}"]
    for field, limit in (("description", 5000), ("category", 60)):
        if field in data and (not isinstance(data[field], str) or len(data[field]) > limit):
            errors[field] = [f"Must be text with at most {limit} characters"]
    if "due_date" in data and data["due_date"] is not None:
        try:
            date.fromisoformat(data["due_date"])
        except (ValueError, TypeError):
            errors["due_date"] = ["Use YYYY-MM-DD or null"]
    if "assigned_to_id" in data and data["assigned_to_id"] is not None:
        if not isinstance(data["assigned_to_id"], int) or data["assigned_to_id"] < 1:
            errors["assigned_to_id"] = ["Must be a positive user ID or null"]
    return errors

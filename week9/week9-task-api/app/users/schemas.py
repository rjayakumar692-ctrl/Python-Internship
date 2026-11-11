def user_update_errors(data):
    errors = {}
    if not isinstance(data, dict) or not data:
        return {"body": ["A non-empty JSON object is required"]}
    unknown = set(data) - {"username", "email"}
    if unknown:
        errors["fields"] = [f"Unknown field(s): {', '.join(sorted(unknown))}"]
    if "username" in data and (not isinstance(data["username"], str) or not 3 <= len(data["username"].strip()) <= 40):
        errors["username"] = ["Username must be 3-40 characters"]
    if "email" in data and (not isinstance(data["email"], str) or "@" not in data["email"]):
        errors["email"] = ["A valid email address is required"]
    return errors

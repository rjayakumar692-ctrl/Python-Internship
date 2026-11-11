from flask_jwt_extended import create_access_token, create_refresh_token
from app.utils.responses import success

def token_response(user, status=200):
    return success({"user": user.to_dict(),
                    "access_token": create_access_token(identity=str(user.id)),
                    "refresh_token": create_refresh_token(identity=str(user.id))}, status)

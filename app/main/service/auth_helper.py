from app.main.model.user import User
from ..service.blacklist_service import save_token

class Auth:

    @staticmethod
    def login_user(data):
        try:
            user = User.objects.get(email=data['email'])
            if user and user.check_password(data['password']):
                auth_token = user.encode_auth_token(str(user['id']))
                if auth_token:
                    response_obj = {
                        "status": "success",
                        "message": "Successfully logged in",
                        "Authorization": auth_token.decode()
                    }
                    return response_obj, 200

            else:
                response_obj = {
                    "status": "fail",
                    "message": "email or password do not match",
                }
                return response_obj, 401
        except Exception as e:
            response_obj = {
                "status": "fail",
                "message": "Try again",
            }
            return response_obj, 500

    @staticmethod
    def logout_user(data):
        if data:
            auth_token = data.split(" ")[1]
        else:
            auth_token = ""

        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                return save_token(token=auth_token)
            else:
                response_obj = {
                    "status": "fail",
                    "message": resp
                }
                return response_obj, 401
        else:
            response_obj = {
                "status": "fail",
                "message": "Provide a valid auth token"
            }
            return response_obj, 403

    @staticmethod
    def get_logged_in_user(new_request):
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if isinstance(resp, str):
                user = User.objects.get(id=resp)
                response_obj = {
                    "status": "success",
                    "data": {
                        "user_id": str(user["id"]),
                        "email": user['email'],
                        "admin": user["admin"],
                        "created_date": user["created_date"]
                    }
                }
                return response_obj, 200
            response_obj = {
                "status": "fail",
                "message": resp["message"]
            }
            return response_obj, 401
        else:
            response_obj = {
                "status": "fail",
                "message": "Provide a valid auth token."
            }
            return response_obj, 401
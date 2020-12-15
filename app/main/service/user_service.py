import uuid
import datetime

from .. import flask_bcrypt

from app.main import db
from app.main.model.user import User

def save_new_user(data):
    user = get_obj_or_404(User, email=data['email'])
    if not user:

        data['created_date'] = datetime.datetime.utcnow()
        data['public_id'] = str(uuid.uuid4())
        data['password_hash'] = flask_bcrypt.generate_password_hash(data['password']).decode('utf-8')
        del data['password']

        User(**data).save()
        new_user = User.objects.get(email=data['email'])

        return generate_token(new_user)

def get_all_users():
    return list(User.objects()), 200

def get_a_user(public_id):
    return User.objects.get(public_id=public_id), 200

def generate_token(user):
    try:
        auth_token = User.encode_auth_token(str(user["id"]))
        response_obj = {
            "status": "success",
            "message": "Successfully registered.",
            "Authorization": auth_token.decode()
        }
        return response_obj, 201
    except Exception as e:
        response_obj = {
            "status": "fail",
            "message": "Some error occured. Please try again"
        }
        return response_obj, 401

def get_obj_or_404(klass, *args, **kwargs):
    try:
        return klass.objects.get(*args, **kwargs)
    except klass.DoesNotExist:
        return None
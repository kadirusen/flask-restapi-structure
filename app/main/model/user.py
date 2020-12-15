from .. import db, flask_bcrypt
from flask_mongoengine.wtf import model_form
from mongoengine import *
from app.main.model.blacklist import BlacklistToken
import datetime
from ..config import key
import jwt

class User(db.Document):
    email = db.StringField(required=True, unique=True)
    created_date = db.DateTimeField(required=True)
    admin = db.BooleanField(required=True, default=False)
    public_id = db.StringField(unique=True)
    username = db.StringField(unique=True)
    password_hash = db.StringField()


    @property
    def password(self):
        raise AttributeError('password: write-pnly field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def encode_auth_token(user_id):

        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds= 5),
                'sub' : user_id
            }
            token = jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
            return token
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            a = key
            payload = jwt.decode(auth_token, key, algorithms=['HS256'])
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again'
            else:
                return payload['sub']

        except jwt.ExpiredSignatureError:
            return {
                "message": "'Signature expired. Please log in again'"
            }
        except jwt.InvalidTokenError:
            return {
                "message": "Invalid token. Please log in again"
            }

    def __repr__(self):
        return "<User '{}'>".format(self.username)

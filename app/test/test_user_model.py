import unittest
import uuid
import datetime

from app.main import db

from app.main import flask_bcrypt
from app.main.model.user import User
from app.test.base import BaseTestCase

class TestUserModel(BaseTestCase):
    def test_encode_auth_token(self):
        user = {
            "email":"test3@test.com",
            "username":"test3",
            "public_id": str(uuid.uuid4()),
            "password_hash": flask_bcrypt.generate_password_hash("test").decode('utf-8'),
            "created_date": datetime.datetime.utcnow()
        }

        User(**user).save()
        created_user = User.objects.get(email=user['email'])
        auth_token = User.encode_auth_token(str(created_user["id"]))
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = {
            "email":"test33@test.com",
            "username": "test33",
            "public_id": str(uuid.uuid4()),
            "password_hash": flask_bcrypt.generate_password_hash("test").decode('utf-8'),
            "created_date": datetime.datetime.utcnow()
        }
        User(**user).save()
        created_user = User.objects.get(email=user['email'])
        auth_token = User.encode_auth_token(str(created_user["id"]))
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token.decode("utf-8")))

if __name__ == "__main__":
    unittest.main()
from flask_testing import TestCase

from app.main import db
from main import app

class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('app.main.config.TestingConfig')
        return app

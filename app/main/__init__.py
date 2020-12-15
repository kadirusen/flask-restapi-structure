from flask import Flask
from flask_mongoengine import MongoEngine

from flask_bcrypt import Bcrypt

from .config import api_config

db = MongoEngine()
flask_bcrypt = Bcrypt()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(api_config[config_name])
    app.config['MONGODB_SETTINGS'] = {
        'db': api_config[config_name].DB_NAME,
        'host': api_config[config_name].DB_HOST,
        'port': api_config[config_name].DB_PORT
    }
    db.init_app(app)
    flask_bcrypt.init_app(app)

    return app
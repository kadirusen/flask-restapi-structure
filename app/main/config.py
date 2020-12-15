import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret12')
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    DB_NAME="user"
    DB_HOST="mongodb"
    DB_PORT=27018

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    DB_NAME="user"
    DB_HOST="mongodb"
    DB_PORT=27018

class ProductionConfig(Config):
    DEBUG = False
    DB_NAME="user"
    DB_HOST="mongodb"
    DB_PORT=27018

api_config = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
from decouple import config
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api

from models import *
from resources.routes import routes


class DevelopmentEnv:
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}"
        f"@localhost:{config('DB_PORT')}/{config('DB_NAME')}"
    )


class ProductionEnv:
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}"
        f"@localhost:{config('DB_PORT')}/{config('DB_NAME')}"
    )


class TestsEnv:
    FLASK_ENV = 'tests'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config('TEST_DB_USER')}:{config('TEST_DB_PASSWORD')}"
        f"@localhost:{config('TEST_DB_PORT')}/{config('TEST_DB_NAME')}"
    )


def create_app(configuration="config.DevelopmentEnv"):
    app = Flask(__name__)
    app.config.from_object(configuration)
    db.init_app(app)
    api = Api(app)
    migrate = Migrate(app, db)
    CORS(app)
    [api.add_resource(*route) for route in routes]
    return app

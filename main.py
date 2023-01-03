from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from db import db
from decouple import config
from models import *

app = Flask(__name__)
app.config.from_object(config('DB_CONFIG'))
db.init_app(app)
api = Api(app)
migrate = Migrate(app, db)


if __name__ == '__main__':
    app.run()


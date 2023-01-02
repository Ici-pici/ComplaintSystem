from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from db import db
from decouple import config

app = Flask(__name__)
app.config.from_object(config('DB_CONFIG'))
api = Api(app)
migrate = Migrate(app, db)


if __name__ == '__main__':
    app.run()


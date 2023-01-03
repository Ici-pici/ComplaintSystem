from decouple import config
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from models import *
from resources.routes import routes

app = Flask(__name__)
app.config.from_object(config('DB_CONFIG'))
db.init_app(app)
api = Api(app)
migrate = Migrate(app, db)


[api.add_resource(*route) for route in routes]

if __name__ == '__main__':
    app.run()


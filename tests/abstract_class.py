from flask_testing import TestCase

from config import create_app
from db import db


class BaseTestClass(TestCase):
    def create_app(self):
        app = create_app('config.TestsEnv')
        return app

    def setUp(self):
        db.init_app(self.create_app())
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


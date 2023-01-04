from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from models.users import ComplainerModel
from managers.auth import AuthManager
from werkzeug.exceptions import BadRequest

class ComplainerManager:
    @staticmethod
    def register(data):
        data['password'] = generate_password_hash(data['password'])
        user = ComplainerModel(**data)
        db.session.add(user)
        token = AuthManager.encode_token(user)
        return token

    @staticmethod
    def login(data):
        user = ComplainerModel.query.filter_by(email=data['email']).first()
        if not user:
            raise BadRequest('Invalid Email')
        if not check_password_hash(user.password, data['password']):
            raise BadRequest('Wrong Password')
        return AuthManager.encode_token(user)


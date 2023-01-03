from werkzeug.security import generate_password_hash
from db import db
from models.users import ComplainerModel
from managers.auth import AuthManager

class ComplainerManager:
    @staticmethod
    def register(data):
        data['password'] = generate_password_hash(data['password'])
        user = ComplainerModel(**data)
        db.session.add(user)
        db.session.commit()
        token = AuthManager.encode_token(user)
        return token

from datetime import datetime, timedelta

import jwt
from decouple import config
from flask_httpauth import HTTPTokenAuth
from jwt import encode
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from werkzeug.exceptions import Unauthorized
from models.users import ComplainerModel, ApproverModel, AdminModel


class AuthManager:
    @staticmethod
    def encode_token(user):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=2),
            'sub': user.id,
            'type': user.__class__.__name__
            }
        return encode(payload,
                      key=config('JWT_KEY'),
                      algorithm='HS256'
                      )

    @staticmethod
    def decode_token(token):
        if not token:
            raise Unauthorized('Token Required')
        try:
            payload = jwt.decode(token, key=config('JWT_KEY'), algorithms=['HS256'])
            return payload['sub'], payload['type']
        except ExpiredSignatureError:
            raise Unauthorized('Expired Token')
        except InvalidSignatureError:
            raise Unauthorized('Invalid Token')


auth = HTTPTokenAuth()

@auth.verify_token
def verify_token(token):
    user_id, role = AuthManager.decode_token(token)
    return eval(f"{role}.query.filter_by(id=user_id).first()")



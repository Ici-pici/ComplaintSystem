from datetime import datetime, timedelta
from jwt import encode, decode, DecodeError
from decouple import config
from flask_httpauth import HTTPTokenAuth
from models.users import ComplainerModel
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from werkzeug.exceptions import BadRequest

class AuthManager:
    @staticmethod
    def encode_token(user):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=2),
            'sub': user.id
            }
        return encode(payload,
                      key=config('JWT_KEY'),
                      algorithm='HS256'
                      )

    @staticmethod
    def decode_token(token):
        try:
            payload = decode(token, key=config('JWT_KEY'), algorithms=['HS256'])
            return payload['sub']
        except ExpiredSignatureError:
            raise BadRequest('Expired Token')
        except InvalidSignatureError:
            raise BadRequest('Invalid Token')
        except DecodeError:
            raise BadRequest('Token Required')


auth = HTTPTokenAuth()

@auth.verify_token
def verify_token(token):
    user_id = AuthManager.decode_token(token)
    return ComplainerModel.query.filter_by(id=user_id).first()



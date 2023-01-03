from datetime import datetime, timedelta
from jwt import encode
from decouple import config
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

from flask import request
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import Forbidden

from managers.auth import auth


def validate_schema(schema):
    def decorator(ref):
        def wrapper(*args, **kwargs):
            data = request.get_json()
            errors = schema().validate(data)
            if errors:
                raise BadRequest(errors)
            return ref(*args, **kwargs)
        return wrapper
    return decorator


def role_required(role):
    def decorated(ref):
        def wrapper(*args, **kwargs):
            user = auth.current_user()
            if not user.role == role:
                raise Forbidden('Permission denied')
            return ref(*args, **kwargs)
        return wrapper
    return decorated

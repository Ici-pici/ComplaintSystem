from flask import request
from werkzeug.exceptions import BadRequest
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

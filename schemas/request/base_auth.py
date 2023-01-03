from marshmallow import Schema, fields, validates, ValidationError
from password_strength import PasswordPolicy
from models.users import ComplainerModel

class BaseAuthSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


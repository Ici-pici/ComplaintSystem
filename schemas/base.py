from marshmallow import Schema, fields, validates, ValidationError
from models.users import ComplainerModel

class BaseAuthSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class BaseComplaintSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    photo_url = fields.Str(required=True)
    amount = fields.Float(required=True)


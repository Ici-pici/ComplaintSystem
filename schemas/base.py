from marshmallow import Schema, fields


class BaseAuthSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class BaseComplaintSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    amount = fields.Float(required=True)


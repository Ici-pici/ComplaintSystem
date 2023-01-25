from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from models.enums import StatusEnum


class ApproverResponseSchema(Schema):
    id = fields.Integer()
    complainer_id = fields.Integer()
    certificate = fields.Str()
    status = EnumField(StatusEnum)
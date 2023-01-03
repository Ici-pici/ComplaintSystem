from marshmallow import Schema, fields
from models.enums import RoleEnum
from marshmallow_enum import EnumField

class ComplaintSchemaResponse(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    photo_url = fields.Str()
    amount = fields.Float()
    status = EnumField(RoleEnum)
    #TODO Do the nested schema

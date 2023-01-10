from marshmallow import Schema, fields
from models.enums import RoleEnum
from marshmallow_enum import EnumField
from schemas.base import BaseComplaintSchema

class ComplaintSchemaResponse(BaseComplaintSchema):
    id = fields.Int()
    status = EnumField(RoleEnum)
    photo_url = fields.Str()
    #TODO Do the nested schema

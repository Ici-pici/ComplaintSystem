from marshmallow import Schema, fields
from models.enums import RoleEnum
from marshmallow_enum import EnumField
from schemas.base import BaseComplaintSchema

class ComplaintSchemaResponse(BaseComplaintSchema):
    id = fields.Int()
    status = EnumField(RoleEnum)
    #TODO Do the nested schema

from marshmallow import fields
from marshmallow_enum import EnumField

from models.enums import RoleEnum
from schemas.base import BaseComplaintSchema


class ComplaintSchemaResponse(BaseComplaintSchema):
    id = fields.Int()
    status = EnumField(RoleEnum)
    photo_url = fields.Str()
    complainer_id = fields.Int()
    #TODO Do the nested schema

from marshmallow import fields, validates, ValidationError

from schemas.base import BaseComplaintSchema


class ComplaintSchemaRequest(BaseComplaintSchema):
    photo = fields.Str(required=True)
    photo_extension = fields.Str(required=True)

    @validates('title')
    def validate_title(self, value):
        if len(value) > 20:
            raise ValidationError('Too long Title')

    @validates('description')
    def validate_description(self, value):
        if not value:
            raise ValidationError('The description is required')

    @validates('photo_url')
    def validate_description(self, value):
        if not value:
            raise ValidationError('The photo is required')

    @validates('amount')
    def validate_description(self, value):
        if value <= 0:
            raise ValidationError('The amount is invalid')


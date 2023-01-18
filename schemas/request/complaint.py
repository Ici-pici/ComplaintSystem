from marshmallow import fields, validates, ValidationError

from schemas.base import BaseComplaintSchema


class ComplaintSchemaRequest(BaseComplaintSchema):
    photo = fields.Str(required=True)
    photo_extension = fields.Str(required=True)

    @validates('photo')
    def validate_photo_url(self, value):
        if not value:
            raise ValidationError('The photo is required')

    @validates('photo_extension')
    def validate_photo_extension(self, value):
        if not value:
            raise ValidationError('The photo extension is required')



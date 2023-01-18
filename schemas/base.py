from marshmallow import Schema, fields, validates, ValidationError


class BaseAuthSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class BaseComplaintSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    amount = fields.Float(required=True)

    @validates('title')
    def test_title(self, value):
        if len(value) == 0:
            raise ValidationError('Title is required.')
        if len(value) > 20:
            raise ValidationError('The title is too long. 20 Chars max.')

    @validates('description')
    def validate_description(self, value):
        if len(value) == 0:
            raise ValidationError('Description is required.')

    @validates('amount')
    def validate_amount(self, value):
        if value <= 0:
            raise ValidationError('The amount cannot be negative number or zero')

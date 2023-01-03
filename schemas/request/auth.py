from marshmallow import Schema, fields, validates, ValidationError
from models.users import ComplainerModel
from schemas.request.base_auth import BaseAuthSchema

class RegisterSchemaRequest(BaseAuthSchema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    phone = fields.Str(required=True)

    @validates('password')
    def validate_password(self, value):
        policy = PasswordPolicy.from_names(
            length=8,
            uppercase=1,
            numbers=1
        )
        errors = policy.test(value)
        if errors:
            raise ValidationError('Invalid Password')

    @validates('first_name')
    def validate_first_name(self, value):
        if len(value) < 2:
            raise ValidationError('Min length is 2 letters')
        for letter in value:
            if letter.isdigit():
                raise ValidationError('The name can consist only of letters')

    @validates('last_name')
    def validate_last_name(self, value):
        if len(value) < 2:
            raise ValidationError('Min length is 2 letters')
        for letter in value:
            if letter.isdigit():
                raise ValidationError('The name can consist only of letters')

    @validates('phone')
    def validate_phone(self, value):
        if value[0] != '+':
            raise ValidationError('Please enter the country code too')
        if len(value) > 14:
            raise ValidationError('The phone number should to be 14 symbols')


    @validates('email')
    def validate_email(self, value):
        repeat = ComplainerModel.query.filter_by(email=value).first()
        if repeat:
            raise ValidationError('This email already present')


class LoginSchemaRequest(BaseAuthSchema):
    pass

from marshmallow import fields, validates, ValidationError
from models.users import ComplainerModel
from schemas.base import BaseAuthSchema
from password_strength import PasswordPolicy

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



class RegisterComplainerSchema(RegisterSchemaRequest):
    sort_code = fields.Str(required=True)
    account_number = fields.Str(required=True)

    @validates('sort_code')
    def validate_sort_code(self, value):
        if not len(value) == 6:
            raise ValidationError('The sort code should be 6 digits long')
        not_digits = [i for i in value if not i.isdigit()]
        if not_digits:
            raise ValidationError('The sort code should consist only of digits')

class LoginSchemaRequest(BaseAuthSchema):
    pass

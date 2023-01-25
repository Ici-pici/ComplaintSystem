import factory

from db import db
from models.enums import RoleEnum
from models.users import ApproverModel, ComplainerModel, AdminModel


class BaseFactory(factory.Factory):
    @classmethod
    def create(cls, **kwargs):
        obj = super().create(**kwargs)
        db.session.add(obj)
        db.session.commit()
        return obj

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    phone = factory.Sequence(lambda n: '123-555-%04d' % n)
    password = factory.Faker('password')


class ApproverFactory(BaseFactory):
    class Meta:
        model = ApproverModel

    certificate = 'https://some_name.s3.amazonaw.com/024fa46e-10c3-491a-b8c7-a85477c80c19.png'
    role = RoleEnum.approver

class ComplainerFactory(BaseFactory):
    class Meta:
        model = ComplainerModel

    sort_code = 111111
    account_number = 28821822
    role = RoleEnum.complainer


class AdminFactory(BaseFactory):
    class Meta:
        model = AdminModel

    role = RoleEnum.admin

import factory

from db import db
from models.users import ApproverModel, ComplainerModel, AdminModel
from models.enums import RoleEnum


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

    certificate = factory.Faker('name')
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

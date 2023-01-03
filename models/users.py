from db import db
from models.enums import RoleEnum

class BaseUserModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(14), nullable=False)
    password = db.Column(db.String(120), nullable=False)


class ApproverModel(BaseUserModel):
    __tablename__ = 'approver_table'

    certificate = db.Column(db.String(255), nullable=False)
    role = db.Column(
        db.Enum(RoleEnum),
        default=RoleEnum.approver,
        nullable=False
    )

class ComplainerModel(BaseUserModel):
    __tablename__ = 'complainer_table'

    role = db.Column(
        db.Enum(RoleEnum),
        default=RoleEnum.complainer,
        nullable=False
    )
    complaints = db.relationship('ComplaintModel', backref='complaint',  lazy='dynamic')


class AdministratorEnum(BaseUserModel):
    __tablename__ = 'administrator_table'

    role = db.Column(
        db.Enum(RoleEnum),
        default=RoleEnum.admin,
        nullable=False
    )

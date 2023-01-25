from sqlalchemy import func

from db import db
from models.enums import StatusEnum


class ApproverRequestModel(db.Model):
    __tablename__ = 'approver_request_table'

    id = db.Column(db.Integer, primary_key=True)
    complainer_id = db.Column(db.Integer, db.ForeignKey('complainer_table.id'))
    certificate = db.Column(db.String(255), nullable=False)
    status = db.Column(
        db.Enum(StatusEnum),
        default=StatusEnum.pending,
        nullable=False
    )
    created_on = db.Column(db.DateTime, server_default=func.now())
    updated_on = db.Column(db.DateTime, onupdate=func.now())
    complainer = db.relationship('ComplainerModel')

from sqlalchemy import func

from db import db
from models.enums import StatusEnum


class ComplaintModel(db.Model):
    __tablename__ = 'complaint_table'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    photo_url = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    created_on = db.Column(db.DateTime, server_default=func.now())
    updated_on = db.Column(db.DateTime, onupdate=func.now())
    status = db.Column(
        db.Enum(StatusEnum),
        default=StatusEnum.pending,
        nullable=False
    )
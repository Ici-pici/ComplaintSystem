from db import db
from sqlalchemy import func

class TransactionModel(db.Model):
    __tablename__ = 'transaction_table'

    id = db.Column(db.Integer, primary_key=True)
    quote_id = db.Column(db.String(50), nullable=False)
    recipient_id = db.Column(db.String(20), nullable=False)
    target_account_id = db.Column(db.String(100), nullable=False)
    transfer_id = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    created_on = db.Column(db.DateTime, server_default=func.now())
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaint_table.id'))
    complaint = db.relationship('ComplaintModel')


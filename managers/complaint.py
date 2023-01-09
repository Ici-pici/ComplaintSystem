from db import db
import uuid
from models.complaints import ComplaintModel
from models.enums import StatusEnum
from models.transactions import TransactionModel
from services.wise import WiseService

wise = WiseService()
class ComplaintManager:
    @staticmethod
    def create(data, user):
        data['complainer_id'] = user.id
        complaint = ComplaintModel(**data)
        db.session.add(complaint)
        db.session.flush()
        ComplaintManager.issue_transaction(
            amount=data['amount'],
            first_name=user.first_name,
            last_name=user.last_name,
            sort_code=user.sort_code,
            account_number=user.account_number,
            complaint_id=complaint.id
            )
        return complaint

    @staticmethod
    def approve(id):
        transaction = TransactionModel.query.filter_by(complaint_id=id).first()
        wise.fund_transfer(transaction.transfer_id)
        ComplaintModel.query.filter_by(id=id).update({'status': StatusEnum.approved})

    @staticmethod
    def reject(id):
        transaction = TransactionModel.query.filter_by(complaint_id=id).first()
        wise.cancel_transfer(transaction.transfer_id)
        ComplaintModel.query.filter_by(id=id).update({'status': StatusEnum.rejected})

    @staticmethod
    def issue_transaction(amount, first_name, last_name, sort_code, account_number, complaint_id):
        quote_id = wise.create_quote('GBP', 'GBP', amount)
        recipient_id = str(
            wise.create_recipient('GBP', first_name=first_name, last_name=last_name, sort_code=sort_code, account_number=account_number))
        custom_uuid = str(uuid.uuid4())
        transfer_id = wise.create_transfer(target_id=recipient_id, quot_id=quote_id, customer_uuid=custom_uuid)
        data = {
            'quote_id': quote_id,
            'recipient_id': recipient_id,
            'target_account_id': custom_uuid,
            'transfer_id': transfer_id,
            'amount': amount,
            'complaint_id': complaint_id,
        }
        transaction = TransactionModel(**data)
        db.session.add(transaction)
        db.session.flush()

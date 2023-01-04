from db import db
from models.complaints import ComplaintModel
from models.enums import StatusEnum
class ComplaintManager:
    @staticmethod
    def create(data, user):
        data['complainer_id'] = user.id
        complaint = ComplaintModel(**data)
        db.session.add(complaint)
        db.session.commit()
        return complaint

    @staticmethod
    def approve(id):
        ComplaintModel.query.filter_by(id=id).update({'status': StatusEnum.approved})

    @staticmethod
    def reject(id):
        ComplaintModel.query.filter_by(id=id).update({'status': StatusEnum.rejected})

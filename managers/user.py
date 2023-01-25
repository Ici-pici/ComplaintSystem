import os
import uuid

from werkzeug import security
from werkzeug.exceptions import BadRequest

import constants
from db import db
from managers.auth import AuthManager
from models.approver_requests import ApproverRequestModel
from models.complaints import ComplaintModel
from models.enums import StatusEnum
from models.transactions import TransactionModel
from models.users import ComplainerModel, ApproverModel, AdminModel
from services.s3 import s3
from utils.helpers import decode_photo, models, get_file_name_from_url


class ComplainerManager:
    @staticmethod
    def register(data):
        data['password'] = security.generate_password_hash(data['password'])
        user = ComplainerModel(**data)
        db.session.add(user)
        db.session.flush()
        token = AuthManager.encode_token(user)
        return token

    @staticmethod
    def login(data):
        user = [y for y in [eval(f"{x}.query.filter_by(email={data}['email']).first()") for x in models] if y]
        if not user:
            raise BadRequest('Invalid Email')
        if not security.check_password_hash(user[0].password, data['password']):
            raise BadRequest('Wrong Password')
        return AuthManager.encode_token(user[0])


class ApproverManager:
    @staticmethod
    def create(data, user):
        requests = ApproverRequestModel.query.filter_by(complainer_id=user.id).all()
        if requests:
            raise BadRequest('This user already has a request for approver')
        ApproverManager.upload_certificate(data)

        approver_request = ApproverRequestModel(
            complainer_id=user.id,
            certificate=data['certificate'],

        )

        db.session.add(approver_request)
        db.session.flush()
        return approver_request

    @staticmethod
    def approve(id):
        approver_request = ApproverRequestModel.query.filter_by(id=id).first()
        complainer = ComplainerModel.query.filter_by(id=approver_request.complainer_id).first()
        approver = ApproverModel(
            first_name=complainer.first_name,
            last_name=complainer.last_name,
            email=complainer.email,
            phone=complainer.phone,
            password=complainer.password,
            certificate=approver_request.certificate
        )

        # When the complainer's role is changed, everything(transactions, complaints, complainer request) is deleted,
        # because of the relationships.
        db.session.delete(approver_request)
        complaints = ComplaintModel.query.filter_by(complainer_id=complainer.id).all()
        for complaint in complaints:
            transaction = TransactionModel.query.filter_by(id=complaint.id).first()
            db.session.delete(transaction)
            db.session.delete(complaint)
        db.session.add(approver)
        db.session.delete(complainer)

    @staticmethod
    def reject(id):
        ApproverRequestModel.query.filter_by(id=id).update({'status': StatusEnum.rejected})
        photo_url = ApproverRequestModel.query.filter_by(id=id).first().certificate
        photo_name = get_file_name_from_url(photo_url)
        s3.remove(key=photo_name)



    @staticmethod
    def remove(id):
        approver = ApproverModel.query.filter_by(id=id).first()
        file_name = get_file_name_from_url(approver.certificate)
        s3.remove(key=file_name)
        db.session.delete(approver)

    @staticmethod
    def upload_certificate(data):
        certificate_name = f'{uuid.uuid4()}.{data["certificate_extension"]}'
        path = os.path.join(constants.TEMP_FOLDER_PATH, certificate_name)
        decode_photo(path, data['certificate'])
        certificate_url = s3.upload(path, certificate_name)
        data['certificate'] = certificate_url
        os.remove(path)


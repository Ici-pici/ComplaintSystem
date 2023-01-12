import os
import uuid

from werkzeug.exceptions import BadRequest
from werkzeug.security import generate_password_hash, check_password_hash

import constants
from db import db
from managers.auth import AuthManager
from models.users import ComplainerModel, ApproverModel
from services.s3 import s3
from utils.helpers import decode_photo


class ComplainerManager:
    @staticmethod
    def register(data):
        data['password'] = generate_password_hash(data['password'])
        user = ComplainerModel(**data)
        db.session.add(user)
        db.session.flush()
        token = AuthManager.encode_token(user)
        return token

    @staticmethod
    def login(data):
        #TODO Need refactor for login in different roles!
        user = ComplainerModel.query.filter_by(email=data['email']).first()
        if not user:
            raise BadRequest('Invalid Email')
        if not check_password_hash(user.password, data['password']):
            raise BadRequest('Wrong Password')
        return AuthManager.encode_token(user)


class ApproverManager:
    @staticmethod
    def create(data, user):
        ApproverManager.upload_certificate(data)

        approver = ApproverModel(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone=user.phone,
            password=user.password,
            certificate=data['certificate'],
            role='approver'
        )
        db.session.add(approver)
        db.session.flush()
        db.session.delete(user)
        return AuthManager.encode_token(approver)

    @staticmethod
    def upload_certificate(data):
        certificate_name = f'{uuid.uuid4()}.{data["certificate_extension"]}'
        path = os.path.join(constants.TEMP_FOLDER_PATH, certificate_name)
        decode_photo(path, data['certificate'])
        certificate_url = s3.upload(path, certificate_name)
        data['certificate'] = certificate_url
        os.remove(path)


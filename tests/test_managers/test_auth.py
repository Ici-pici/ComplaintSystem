from tests.abstract_class import BaseTestClass
from models.users import ComplainerModel
from unittest.mock import patch
from werkzeug import security
from tests.helper import token_custom, hash_custom, ordinary_mock
from managers.auth import AuthManager
from db import db
from tests.factories import ComplainerFactory, ApproverFactory, AdminFactory
from models.enums import RoleEnum
from tests.helper import create_token, uuid_custom, test_photo, jwt_decode_mock
from managers.complainer import ApproverManager
from services.s3 import S3Service
import jwt
import constants
import os
from models.users import ApproverModel
from decouple import config

headers = {
            'Content-Type': 'application/json'
        }

class TestRegisterComplainerManager(BaseTestClass):
    URL = '/complainer_register'

    @staticmethod
    def check_db_len(length):
        complainers = ComplainerModel.query.all()
        assert len(complainers) == length

    @patch.object(db.session, 'flush')
    @patch.object(security, 'generate_password_hash', return_value=hash_custom())
    @patch.object(AuthManager, 'encode_token', return_value=token_custom())
    def test_register_happy_path(self, encode_token_mock, generate_pass_hash_mock, flush_mock):
        self.check_db_len(0)

        data = {
            'first_name': 'TestName',
            'last_name': 'TestName',
            'email': 'test@gmail.com',
            'phone': '+11111111111111',
            'password': 'TestPassword13',
            'sort_code': '231470',
            'account_number': '28821822'
        }

        response = self.client.post(TestRegisterComplainerManager.URL, headers=headers, json=data)
        self.check_db_len(1)
        assert response.json == {'token': token_custom()}
        assert response.status_code == 201
        user = ComplainerModel.query.all()[0]
        encode_token_mock.assert_called_once_with(user)
        generate_pass_hash_mock.assert_called_once_with(data['password'])
        flush_mock.assert_called_once()


class TestLoginComplainerManager(BaseTestClass):
    URL = '/login'

    def abstract_test(self, factory_reference, status_code=200, data=None):
        user = factory_reference()
        if not data:
            data = {
                'email': user.email,
                'password': user.password
            }
        response = self.client.post(TestLoginComplainerManager.URL, headers=headers, json=data)
        assert response.status_code == status_code
        return response, data, user

    @patch.object(AuthManager, 'encode_token', return_value=token_custom())
    @patch.object(security, 'check_password_hash', return_value=True)
    def test_login_happy_path(self, check_password_hash_mock, encode_token_mock):
        response, data, user = self.abstract_test(ComplainerFactory)
        assert response.json == {'token': token_custom()}
        user = ComplainerModel.query.all()[0]
        check_password_hash_mock.assert_called_once_with(user.password, data['password'])
        encode_token_mock.assert_called_once_with(user)

    @patch('werkzeug.security.check_password_hash', ordinary_mock)
    def test_login_as_complainer(self):
        self.abstract_test(ComplainerFactory)

    @patch('werkzeug.security.check_password_hash', ordinary_mock)
    def test_login_as_approver(self):
        self.abstract_test(ApproverFactory)

    @patch('werkzeug.security.check_password_hash', ordinary_mock)
    def test_login_as_admin(self):
        self.abstract_test(AdminFactory)

    def test_login_with_absent_user(self):
        data = {
            'email': 'wrong@gmail.com',
            'password': 'SomePassword22'
        }
        response, data, user = self.abstract_test(ApproverFactory, status_code=400, data=data)
        assert response.json['message'] == 'Invalid Email'

    @patch.object(security, 'check_password_hash', return_value=False)
    def test_login_with_wrong_password(self, check_password_hash_mock):
        response, data, user = self.abstract_test(ApproverFactory, status_code=400)
        assert response.json['message'] == 'Wrong Password'
        check_password_hash_mock.assert_called_once_with(user.password, data['password'])


class TestRegisterApproverManager(BaseTestClass):
    URL = '/approver_register'

    def db_checker(self, complainer_len, approver_len):
        complainers = ComplainerModel.query.all()
        assert len(complainers) == complainer_len
        approvers = ApproverModel.query.all()
        assert len(approvers) == approver_len

    def abstract_test(self, photo, status_code, message):
        complainer = ComplainerFactory()
        token = create_token(complainer)

        data = {
            'certificate': photo,
            'certificate_extension': 'png'
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        self.db_checker(1, 0)

        response = self.client.post(TestRegisterApproverManager.URL, headers=headers, json=data)
        assert response.status_code == status_code
        assert response.json == message

        return response, data, complainer

    @patch('uuid.uuid4', uuid_custom)
    @patch.object(db.session, 'flush')
    @patch.object(os, 'remove')
    @patch.object(jwt, 'decode', return_value=jwt_decode_mock())
    @patch.object(AuthManager, 'encode_token', return_value=token_custom())
    @patch.object(S3Service, 'upload', return_value='testurl.com')
    def test_register_approver_happy_path(self, s3_mock, encode_token_mock, jwt_mock, os_remove_mock, flush_mock):
        expected_response = {
            'token': token_custom()
        }

        response, data, complainer = self.abstract_test(test_photo, 200, expected_response)

        self.db_checker(0, 1)

        certificate_name = uuid_custom() + f'.{data["certificate_extension"]}'
        path = os.path.join(constants.TEMP_FOLDER_PATH, certificate_name)
        s3_mock.assert_called_once_with(path, certificate_name)

        encode_token_mock.assert_called()

        jwt_mock.assert_called_once_with(token_custom(), key=config('JWT_KEY'), algorithms=['HS256'])

        os_remove_mock.assert_called_once_with(path)

        flush_mock.assert_called_once_with()

    def test_register_approver_with_wrong_photo_type(self):
        expected_response = {
            'message': 'Photo decoding failed'
        }

        self.abstract_test('WrongPhoto', 400, expected_response)


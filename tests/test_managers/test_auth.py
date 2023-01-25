import os
from unittest.mock import patch

from werkzeug import security

import constants
from db import db
from managers.auth import AuthManager
from managers.complaint import ComplaintManager
from models.approver_requests import ApproverRequestModel
from models.complaints import ComplaintModel
from models.enums import StatusEnum
from models.transactions import TransactionModel
from models.users import ApproverModel
from models.users import ComplainerModel
from services.s3 import S3Service
from tests.abstract_class import BaseTestClass
from tests.factories import ComplainerFactory, ApproverFactory, AdminFactory
from tests.helper import create_token, uuid_custom, test_photo
from tests.helper import token_custom, hash_custom, ordinary_mock

headers = {
            'Content-Type': 'application/json'
        }

def headers2(token):
    return {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

def transaction_data():
    return {
            'quote_id': 11111,
            'recipient_id': 11111,
            'target_account_id': 1,
            'transfer_id': 11111,
            'amount': 1,
            'complaint_id': 1,
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


class TestApproverManager(BaseTestClass):
    CREATE_ENDPOINT = '/approver_register'

    def db_checker(self, the_requests, complainers):
        requests = ApproverRequestModel.query.all()
        assert len(requests) == the_requests
        complainer = ComplainerModel.query.all()
        assert len(complainer) == complainers

    def register_abstract_test(self, user, photo, expected_response, status_code, db_requests_count=0):
        token = create_token(user)
        data = {
            'certificate': photo,
            'certificate_extension': 'png'
        }

        self.db_checker(db_requests_count, 1)
        response = self.client.post(TestApproverManager.CREATE_ENDPOINT, headers=headers2(token), json=data)
        assert response.json == expected_response
        assert response.status_code == status_code
        return response, user, data


    @patch('uuid.uuid4', uuid_custom)
    @patch.object(S3Service, 'upload', return_value='https://some_name.s3.amazonaw.com/024fa46e-10c3-491a-b8c7-a85477c80c19.png')
    @patch.object(os, 'remove')
    def test_create_approver_request_method_happy_path(self, os_mock, s3_mock):
        expected_response = {
            'status': StatusEnum.pending.name,
            'id': 1,
            'complainer_id': 1,
            'certificate': 'https://some_name.s3.amazonaw.com/024fa46e-10c3-491a-b8c7-a85477c80c19.png'
        }
        user = ComplainerFactory()
        response, user, data = self.register_abstract_test(user, test_photo, expected_response, 201)

        certificate_name = uuid_custom() + f'.{data["certificate_extension"]}'
        path = os.path.join(constants.TEMP_FOLDER_PATH, certificate_name)
        s3_mock.assert_called_once_with(path, certificate_name)
        os_mock.assert_called_once_with(path)
        return user

    def test_create_approver_request_with_invalid_photo(self):
        expected_response = {'message': 'Photo decoding failed'}
        user = ComplainerFactory()
        self.register_abstract_test(user, 'TestPhoto', expected_response, 400)

    def test_for_dublicating_in_create_approver_request(self):
        user = self.test_create_approver_request_method_happy_path()
        expected_response = {
            'message': 'This user already has a request for approver'
        }
        self.register_abstract_test(user, test_photo, expected_response, 400, 1)


    @patch.object(S3Service, 'upload', return_value='site.com')
    @patch.object(ComplaintManager, 'issue_transaction', return_value=transaction_data())
    def test_approve_method(self, issue_transaction_mock, s3_mock):
        # Getting already created request
        user = self.test_create_approver_request_method_happy_path()

        # Creating a complaint and transaction to check if they will be deleted leter.
        user_token = create_token(user)
        data = {
            'title': 'TestTitle',
            'description': 'TestDescription',
            'photo': test_photo,
            'amount': 10,
            'photo_extension': 'png'
        }
        self.client.post('/make_complaint', headers=headers2(user_token), json=data)

        assert len(ComplainerModel.query.all()) == 1
        assert len(TransactionModel.query.all()) == 1
        assert len(ComplaintModel.query.all()) == 1
        assert len(ApproverRequestModel.query.all()) == 1

        admin = AdminFactory()
        admin_token = create_token(admin)
        response = self.client.put(f'/approver_request/{user.id}/approve', headers=headers2(admin_token))
        assert response.status_code == 200
        assert response.json == 204
        assert len(ApproverRequestModel.query.all()) == 0
        assert len(ApproverModel.query.all()) == 1
        assert len(ComplainerModel.query.all()) == 0
        assert len(TransactionModel.query.all()) == 0
        assert len(ComplaintModel.query.all()) == 0

    @patch.object(S3Service, 'remove')
    def test_reject_method(self, s3_mock):
        # Getting already created request
        user = self.test_create_approver_request_method_happy_path()
        approver_request = ApproverRequestModel.query.all()[0]
        admin = AdminFactory()
        token = create_token(admin)
        response = self.client.put(f'/approver_request/{approver_request.id}/reject', headers=headers2(token))
        assert approver_request.status == StatusEnum.rejected
        assert response.json == 204
        assert response.status_code == 200
        s3_mock.assert_called_once()

    @patch.object(S3Service, 'remove')
    def test_remove_approver_method(self, s3_mock):
        approver = ApproverFactory()
        admin = AdminFactory()
        token = create_token(admin)
        assert len(ApproverModel.query.all()) == 1
        response = self.client.put(f'/remove_approver/{approver.id}', headers=headers2(token))
        assert response.json == 204
        assert response.status_code == 200
        assert len(ApproverModel.query.all()) == 0
        s3_mock.assert_called_once()




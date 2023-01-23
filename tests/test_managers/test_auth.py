from tests.abstract_class import BaseTestClass
from models.users import ComplainerModel
from unittest.mock import patch
from werkzeug import security
from tests.helper import token_custom, hash_custom, ordinary_mock
from managers.auth import AuthManager
from db import db
from tests.factories import ComplainerFactory, ApproverFactory, AdminFactory
from models.enums import RoleEnum
from tests.helper import create_token
from managers.complainer import ApproverManager

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
        print()

    @patch.object(security, 'check_password_hash', return_value=False)
    def test_login_with_wrong_password(self, check_password_hash_mock):
        response, data, user = self.abstract_test(ApproverFactory, status_code=400)
        assert response.json['message'] == 'Wrong Password'
        check_password_hash_mock.assert_called_once_with(user.password, data['password'])


class TestRegisterApproverManager(BaseTestClass):
    URL = '/approver_register'

    @patch.object(ApproverManager, 'upload_certificate', return_value='someurl.com')
    def test_register_approver_happy_path(self, upload_certificate_mock):
        #TODO The mock is not correct. We have to mock every part of the upload_certificate, if we want to cover more things.

        complainer = ComplainerFactory()
        token = create_token(complainer)

        data = {
            'certificate': 'SomeCertificate',
            'certificate_extension': 'png'
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        response = self.client.post(TestRegisterApproverManager.URL, headers=headers, json=data)



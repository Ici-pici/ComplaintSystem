from flask_testing import TestCase
from db import db
from config import create_app
import json
from tests.factories import ApproverFactory, ComplainerFactory
from tests.helper import create_token

LOGIN_REQUIRED_ENDPOINTS = (
            ('post', '/approver_register'),
            ('post', '/make_complaint'),
            ('put', '/complaint/1/approve'),
            ('put', '/complaint/1/reject')
        )

COMPLAINER_ROLE_REQUIRED_ENDPOINTS = (
            ('post', '/approver_register'),
            ('post', '/make_complaint')
        )

APPROVER_ROLE_REQUIREMENT_ENDPOINTS = (
            ('put', '/complaint/1/approve'),
            ('put', '/complaint/1/reject')
        )

class TestApp(TestCase):
    #TODO Token Expired with Patch
    #TODO Administration test when we have admins endpoints

    def create_app(self):
        return create_app('config.TestsEnv')

    def setUp(self):
        db.init_app(self.create_app())
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def endpoint_iteration(self, endpoints, message, assert_type, headers=None):

        if not headers:
            headers = {}

        for request, url in endpoints:
            response = eval(f"self.client.{request}('{url}', headers={headers})")
            assert_type(response)
            self.assertEqual(response.json, {'message': message})

    def test_all_endpoints_that_require_authorization_without_token(self):
        self.endpoint_iteration(LOGIN_REQUIRED_ENDPOINTS, 'Token Required', self.assert_401)

    def test_all_endpoints_that_require_authorization_with_wrong_token(self):
        headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
                             'eyJleHAiOjE2NzM2OTk2NjEsInN1YiI6MiwidHlwZSI6IkFwcHJvdmVyTW9kZWwifQ.'
                             'dvWXJfgvE9IcvCjU9IfjMW80yaGg93JRYC-OPOYVjX0'
        }

        self.endpoint_iteration(LOGIN_REQUIRED_ENDPOINTS, 'Invalid Token', self.assert_401, headers)

    def test_all_endpoints_that_require_complainer_role(self):
        user = ApproverFactory()
        token = create_token(user)
        headers = {'Authorization': f"Bearer {token}"}
        self.endpoint_iteration(COMPLAINER_ROLE_REQUIRED_ENDPOINTS, 'Permission denied', self.assert403, headers=headers)

    def test_all_endpoints_that_require_approver_role(self):
        complainer = ComplainerFactory()
        token = create_token(complainer)
        headers = {'Authorization': f"Bearer {token}"}
        self.endpoint_iteration(APPROVER_ROLE_REQUIREMENT_ENDPOINTS, 'Permission denied', self.assert403, headers)


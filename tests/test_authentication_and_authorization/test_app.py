from tests.abstract_class import BaseTestClass
from tests.factories import ApproverFactory, ComplainerFactory
from tests.helper import create_token

LOGIN_REQUIRED_ENDPOINTS = (
            ('post', '/approver_register'),
            ('post', '/make_complaint'),
            ('put', '/complaint/1/approve'),
            ('put', '/complaint/1/reject'),
            ('put', '/approver_request/1/approve'),
            ('put', '/approver_request/1/reject'),
            ('put', '/remove_approver/1')
        )

COMPLAINER_ROLE_REQUIRED_ENDPOINTS = (
            ('post', '/approver_register'),
            ('post', '/make_complaint')
        )

APPROVER_ROLE_REQUIREMENT_ENDPOINTS = (
            ('put', '/complaint/1/approve'),
            ('put', '/complaint/1/reject'),
            ('put', '/remove_approver/1')
        )

ADMIN_ROLE_REQUIREMNT_ENDPOINTS = (
            ('put', '/approver_request/1/approve'),
            ('put', '/approver_request/1/reject'),
)

class TestApp(BaseTestClass):
    #TODO Token Expired with Patch

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
        self.endpoint_iteration(APPROVER_ROLE_REQUIREMENT_ENDPOINTS, 'Permission denied', self.assert403, headers=headers)

    def test_all_endpoints_that_require_admin_role(self):
        approver = ApproverFactory()
        token = create_token(approver)
        headers = {'Authorization': f"Bearer {token}"}
        self.endpoint_iteration(ADMIN_ROLE_REQUIREMNT_ENDPOINTS, 'Permission denied', self.assert_403, headers=headers)


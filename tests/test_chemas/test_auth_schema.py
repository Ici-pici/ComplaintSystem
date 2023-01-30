from unittest.mock import patch

from werkzeug import security

from tests.abstract_class import BaseTestClass
from tests.factories import ComplainerFactory
from tests.helper import create_token
from tests.helper import ordinary_mock

headers = {
    'Content-Type': 'application/json'
}
class TestAuthSchemaRegister(BaseTestClass):
    REGISTER_URL = '/complainer_register'
    VALID_DATA = {
            'email': 'test@gmail.com',
            'password': 'SomeTestPass3',
            'first_name': 'Test Name',
            'last_name': 'Test Last Name',
            'phone': '+11111111111111',
            'account_number': '11111111',
            'sort_code': '111111'
        }

    def abstract_test(self, data, status_code, expected_response):
        response = self.client.post(TestAuthSchemaRegister.REGISTER_URL, headers=headers, json=data)
        assert response.status_code == status_code
        assert response.json['message'] == expected_response

    def test_register_schema_without_data(self):
        data = {}
        expected_response = {
            'email': ['Missing data for required field.'],
            'phone': ['Missing data for required field.'],
            'last_name': ['Missing data for required field.'],
            'account_number': ['Missing data for required field.'],
            'sort_code': ['Missing data for required field.'],
            'first_name': ['Missing data for required field.'],
            'password': ['Missing data for required field.']
        }
        self.abstract_test(data, 400, expected_response)

    def test_register_schema_with_invalid_email(self):
        data = TestAuthSchemaRegister.VALID_DATA.copy()
        data['email'] = 'testgmail.com'
        expected_response = {
            'email': ['Not a valid email address.']
        }
        self.abstract_test(data, 400, expected_response)

    def test_register_schema_with_repeated_email(self):
        user = ComplainerFactory()
        data = TestAuthSchemaRegister.VALID_DATA.copy()
        data['email'] = user.email

        expected_response = {
            'email': ['This email already present']
        }
        self.abstract_test(data, 400, expected_response)

    def test_short_password(self):
        data = TestAuthSchemaRegister.VALID_DATA.copy()
        data['password'] = 'Short3'
        expected_response = {
            'password': ['Invalid Password']
        }
        self.abstract_test(data, 400, expected_response)

    def test_password_without_uppercase_letters(self):
        data = TestAuthSchemaRegister.VALID_DATA.copy()
        data['password'] = 'password4'
        expected_response = {
            'password': ['Invalid Password']
        }
        self.abstract_test(data, 400, expected_response)

    def test_password_without_numbers(self):
        data = TestAuthSchemaRegister.VALID_DATA.copy()
        data['password'] = 'Password'
        expected_response = {
            'password': ['Invalid Password']
        }
        self.abstract_test(data, 400, expected_response)

    def test_password_with_incorrect_data_type(self):
        data = TestAuthSchemaRegister.VALID_DATA.copy()
        data['password'] = 5
        expected_response = {
            'password': ['Not a valid string.']
        }
        self.abstract_test(data, 400, expected_response)


    def test_first_name_with_incorrect_data_type(self):
        data = TestAuthSchemaRegister.VALID_DATA.copy()
        data['first_name'] = 2
        expected_response = {
            'first_name': ['Not a valid string.']
        }
        self.abstract_test(data, 400, expected_response)

    def test_first_name_with_one_letter(self):
        data = TestAuthSchemaRegister.VALID_DATA.copy()
        data['first_name'] = 'a'
        expected_response = {
            'first_name': ['Min length is 2 letters']
        }
        self.abstract_test(data, 400, expected_response)

    def test_first_name_with_for_max_length(self):
        data = TestAuthSchemaRegister.VALID_DATA.copy()
        data['first_name'] = 'aaaaaaaaaaaaaaaaaaaaa'
        expected_response = {
            'first_name': ['20 letters is maximum length']
        }
        self.abstract_test(data, 400, expected_response)

    def test_first_name_with_digits(self):
        data = TestAuthSchemaRegister.VALID_DATA.copy()
        data['first_name'] = 'Test Name 2'
        expected_response = {
            'first_name': ['The name can consist only of letters']
        }
        self.abstract_test(data, 400, expected_response)

    def test_last_name_with_invalid_data_type(self):
        data = TestAuthSchemaRegister.VALID_DATA.copy()
        data['last_name'] = 3
        expected_response = {
            'last_name': ['Not a valid string.']
        }
        self.abstract_test(data, 400, expected_response)

    def test_last_name_with_one_letter(self):
        data = TestAuthSchemaRegister.VALID_DATA.copy()
        data['last_name'] = 'a'
        expected_response = {
            'last_name': ['Min length is 2 letters']
        }
        self.abstract_test(data, 400, expected_response)

    def test_last_name_with_for_max_length(self):
        data = TestAuthSchemaRegister.VALID_DATA.copy()
        data['last_name'] = 'aaaaaaaaaaaaaaaaaaaaa'
        expected_response = {
            'last_name': ['20 letters is maximum length']
        }
        self.abstract_test(data, 400, expected_response)

    def test_last_name_with_digits(self):
        data = TestAuthSchemaRegister.VALID_DATA.copy()
        data['last_name'] = 'Test Name 2'
        expected_response = {
            'last_name': ['The name can consist only of letters']
        }
        self.abstract_test(data, 400, expected_response)


    def test_phone_with_invalid_data_type(self):
        data = TestAuthSchemaRegister.VALID_DATA.copy()
        data['phone'] = 1
        expected_response = {
            'phone': ['Not a valid string.']
        }
        self.abstract_test(data, 400, expected_response)

    def test_phone_that_do_not_start_with_plus_sign(self):
        data = TestAuthSchemaRegister.VALID_DATA.copy()
        data['phone'] = '111111111111111'
        expected_response = {
            'phone': ['Please enter the country code too']
        }
        self.abstract_test(data, 400, expected_response)

    def test_phone_with_wrong_length(self):
        data = TestAuthSchemaRegister.VALID_DATA.copy()
        data['phone'] = '+111111111111111'
        expected_response = {
            'phone': ['The phone number should to be 14 symbols']
        }
        self.abstract_test(data, 400, expected_response)

    def test_sort_code_with_invalid_data_type(self):
        data = TestAuthSchemaRegister.VALID_DATA.copy()
        data['sort_code'] = 5
        expected_response = {
            'sort_code': ['Not a valid string.']
        }
        self.abstract_test(data, 400, expected_response)

    def test_sort_code_with_invalid_length(self):
        data = TestAuthSchemaRegister.VALID_DATA.copy()
        data['sort_code'] = '66666'
        expected_response = {
            'sort_code': ['The sort code should be 6 digits long']
        }
        self.abstract_test(data, 400, expected_response)

    def test_sort_code_with_letters(self):
        data = TestAuthSchemaRegister.VALID_DATA.copy()
        data['sort_code'] = '66666A'
        expected_response = {
            'sort_code': ['The sort code should consist only of digits']
        }
        self.abstract_test(data, 400, expected_response)

    def test_account_number_with_invalid_data_type(self):
        data = TestAuthSchemaRegister.VALID_DATA.copy()
        data['account_number'] = 5
        expected_response = {
            'account_number': ['Not a valid string.']
        }
        self.abstract_test(data, 400, expected_response)

    def test_account_number_with_incorrect_length(self):
        data = TestAuthSchemaRegister.VALID_DATA.copy()
        data['account_number'] = '111111111'
        expected_response = {
            'account_number': ['Invalid Account Number']
        }
        self.abstract_test(data, 400, expected_response)


class TestAuthSchemaRegisterApprover(BaseTestClass):
    URL = '/approver_register'

    def abstract_test(self, data, expected_response):
        user = ComplainerFactory()
        token = create_token(user)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        response = self.client.post(TestAuthSchemaRegisterApprover.URL, headers=headers, json=data)
        assert response.json['message'] == expected_response
        assert response.status_code == 400

    def test_register_without_data(self):
        data = {}
        expected_response = {
            'certificate': ['Missing data for required field.'],
            'certificate_extension': ['Missing data for required field.']
        }
        self.abstract_test(data, expected_response)

    def test_register_with_wrong_data_types(self):
        data = {
            'certificate': 5,
            'certificate_extension': 5
        }
        expected_response = {
            'certificate': ['Not a valid string.'],
            'certificate_extension': ['Not a valid string.']
        }
        self.abstract_test(data, expected_response)


class TestAuthSchemaLogin(BaseTestClass):
    LOGIN_URL = '/login'
    VALID_DATA = {
        'email': 'test@gmail.com',
        'password': 'TestPass26'
    }

    def abstract_test(self, data, expected_response):
        headers = {
            'Content-Type': 'application/json'
        }
        response = self.client.post(TestAuthSchemaLogin.LOGIN_URL, headers=headers, json=data)
        assert response.json['message'] == expected_response
        assert response.status_code == 400

    def test_login_with_empty_data(self):
        data = {}
        expecter_response = {
            'email': ['Missing data for required field.'],
            'password': ['Missing data for required field.']
        }
        self.abstract_test(data, expecter_response)

    def test_with_invalid_email(self):
        data = TestAuthSchemaLogin.VALID_DATA.copy()
        data['email'] = 'testgmail.com'
        expected_response = {
            'email': ['Not a valid email address.']
        }
        self.abstract_test(data, expected_response)

    def test_password_with_invalid_data_type(self):
        data = TestAuthSchemaLogin.VALID_DATA.copy()
        data['password'] = 5
        expected_response = {
            'password': ['Not a valid string.']
        }
        self.abstract_test(data, expected_response)

    @patch.object(security, 'check_password_hash', return_value=ordinary_mock())
    def test_login_happy_path(self, check_pass_hash_mock):
        user = ComplainerFactory()
        data = {
            'email': user.email,
            'password': user.password
        }
        response = self.client.post(TestAuthSchemaLogin.LOGIN_URL, headers=headers, json=data)
        assert response.status_code == 200
        check_pass_hash_mock.assert_called_once_with(user.password, user.password)






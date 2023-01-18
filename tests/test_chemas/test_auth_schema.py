from tests.abstract_class import BaseTestClass
from tests.factories import ComplainerFactory

class TestAuthSchemas(BaseTestClass):
    REGISTER_URL = '/complainer_register'
    VALID_DATA = {
            'email': 'test@gmail.com',
            'password': 'SomeTestPass3',
            'first_name': 'Test Name',
            'last_name': 'Test Last Name',
            'phone': '+11111111111111',
            'account_number': '111111111',
            'sort_code': '111111'
        }

    def abstract_test(self, data, status_code, expected_response):
        headers = {
            'Content-Type': 'application/json'
        }
        response = self.client.post(TestAuthSchemas.REGISTER_URL, headers=headers, json=data)
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
        data = TestAuthSchemas.VALID_DATA
        data['email'] = 'testgmail.com'
        expected_response = {
            'email': ['Not a valid email address.']
        }
        self.abstract_test(data, 400, expected_response)

    def test_register_schema_with_repeated_email(self):
        user = ComplainerFactory()
        data = TestAuthSchemas.VALID_DATA
        data['email'] = user.email

        expected_response = {
            'email': ['This email already present']
        }
        self.abstract_test(TestAuthSchemas.VALID_DATA, 400, expected_response)

    def test_short_password(self):
        data = TestAuthSchemas.VALID_DATA
        data['password'] = 'Short3'
        expected_response = {
            'password': ['Invalid Password']
        }
        self.abstract_test(data, 400, expected_response)

    def test_password_without_uppercase_letters(self):
        data = TestAuthSchemas.VALID_DATA
        data['password'] = 'password4'
        expected_response = {
            'password': ['Invalid Password']
        }
        self.abstract_test(data, 400, expected_response)

    def test_password_without_numbers(self):
        data = TestAuthSchemas.VALID_DATA
        data['password'] = 'Password'
        expected_response = {
            'password': ['Invalid Password']
        }
        self.abstract_test(data, 400, expected_response)

    def test_first_name_with_one_letter(self):
        data = TestAuthSchemas.VALID_DATA
        data['first_name'] = 'a'
        expected_response = {
            'first_name': ['Min length is 2 letters']
        }
        self.abstract_test(data, 400, expected_response)

    def test_first_name_with_digits(self):
        data = TestAuthSchemas.VALID_DATA
        data['first_name'] = 'Test Name 2'
        expected_response = {
            'first_name': ['The name can consist only of letters']
        }
        self.abstract_test(data, 400, expected_response)

    def test_last_name_with_one_letter(self):
        data = TestAuthSchemas.VALID_DATA
        data['last_name'] = 'a'
        expected_response = {
            'last_name': ['Min length is 2 letters']
        }
        self.abstract_test(data, 400, expected_response)

    def test_last_name_with_digits(self):
        data = TestAuthSchemas.VALID_DATA
        data['last_name'] = 'Test Name 2'
        expected_response = {
            'last_name': ['The name can consist only of letters']
        }
        self.abstract_test(data, 400, expected_response)


    def test_phone_that_do_not_start_with_plus_sign(self):
        data = TestAuthSchemas.VALID_DATA
        data['phone'] = '111111111111111'
        expected_response = {
            'phone': ['Please enter the country code too']
        }
        self.abstract_test(data, 400, expected_response)

    def test_phone_with_wrong_length(self):
        data = TestAuthSchemas.VALID_DATA
        data['phone'] = '+111111111111111'
        expected_response = {
            'phone': ['The phone number should to be 14 symbols']
        }
        self.abstract_test(data, 400, expected_response)

    def test_sort_code_with_invalid_length(self):
        data = TestAuthSchemas.VALID_DATA
        data['sort_code'] = '66666'
        expected_response = {
            'sort_code': ['The sort code should be 6 digits long']
        }
        self.abstract_test(data, 400, expected_response)

    def test_sort_code_with_letters(self):
        data = TestAuthSchemas.VALID_DATA
        data['sort_code'] = '66666A'
        expected_response = {
            'sort_code': ['The sort code should consist only of digits']
        }
        self.abstract_test(data, 400, expected_response)



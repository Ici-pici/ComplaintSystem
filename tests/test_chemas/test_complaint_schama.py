from tests.abstract_class import BaseTestClass
from tests.factories import ComplainerFactory
from tests.helper import create_token
from tests.helper import test_photo

class TestComplaintSchema(BaseTestClass):
    URL = '/make_complaint'
    VALID_DATA = {
        'title': 'Test title',
        'description': 'Test description',
        'amount': 10,
        'photo': test_photo,
        'photo_extension': 'png'
    }


    def abstract_test(self, data, expected_response, status_code):
        user = ComplainerFactory()
        token = create_token(user)
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        response = self.client.post(
            TestComplaintSchema.URL,
            headers=headers,
            json=data
        )
        assert response.status_code == status_code
        assert response.json['message'] == expected_response

    def test_chama_without_data(self):


        data = {}
        expected_response = {
            'photo_extension': ['Missing data for required field.'],
            'description': ['Missing data for required field.'],
            'title': ['Missing data for required field.'],
            'photo': ['Missing data for required field.'],
            'amount': ['Missing data for required field.']
        }

        self.abstract_test(data, expected_response, 400)


    def test_title_with_wrong_data_type(self):
        data = TestComplaintSchema.VALID_DATA.copy()
        data['title'] = 2
        expected_response = {
            'title': ['Not a valid string.'],
        }
        self.abstract_test(data, expected_response, 400)

    def test_title_required(self):
        data = TestComplaintSchema.VALID_DATA.copy()
        data['title'] = ''
        expected_response = {
            'title': ['Title is required.'],
        }
        self.abstract_test(data, expected_response, 400)

    def test_title_too_long(self):
        data = TestComplaintSchema.VALID_DATA.copy()
        data['title'] = 'aaaaaaaaaaaaaaaaaaaaa'
        expected_response = {
            'title': ['The title is too long. 20 Chars max.'],
        }
        self.abstract_test(data, expected_response, 400)

    def test_description_with_wrong_data_type(self):
        data = TestComplaintSchema.VALID_DATA.copy()
        data['description'] = 1
        expected_response = {
            'description': ['Not a valid string.'],
        }
        self.abstract_test(data, expected_response, 400)

    def test_description_empty_string(self):
        data = TestComplaintSchema.VALID_DATA.copy()
        data['description'] = ''
        expected_response = {
            'description': ['Description is required.'],
        }
        self.abstract_test(data, expected_response, 400)

    def test_amount_with_wrong_data_type(self):
        data = TestComplaintSchema.VALID_DATA.copy()
        data['amount'] = "a"
        expected_response = {
            'amount': ['Not a valid number.'],
        }
        self.abstract_test(data, expected_response, 400)

    def test_amount_with_negative_number(self):
        data = TestComplaintSchema.VALID_DATA.copy()
        data['amount'] = -1
        expected_response = {
            'amount': ['The amount cannot be negative number or zero'],
        }
        self.abstract_test(data, expected_response, 400)

    def test_amount_with_zero(self):
        data = TestComplaintSchema.VALID_DATA.copy()
        data['amount'] = 0
        expected_response = {
            'amount': ['The amount cannot be negative number or zero'],
        }
        self.abstract_test(data, expected_response, 400)

    def test_photo_with_wrong_data_type(self):
        data = TestComplaintSchema.VALID_DATA.copy()
        data['photo'] = 1
        expected_response = {
            'photo': ['Not a valid string.'],
        }
        self.abstract_test(data, expected_response, 400)

    def test_photo_with_empty_string(self):
        data = TestComplaintSchema.VALID_DATA.copy()
        data['photo'] = ''
        expected_response = {
            'photo': ['The photo is required'],
        }
        self.abstract_test(data, expected_response, 400)

    def test_photo_extension_with_invalid_data_type(self):
        data = TestComplaintSchema.VALID_DATA.copy()
        data['photo_extension'] = 1
        expected_response = {
            'photo_extension': ['Not a valid string.'],
        }
        self.abstract_test(data, expected_response, 400)

    def test_photo_extension_with_empty_string(self):
        data = TestComplaintSchema.VALID_DATA.copy()
        data['photo_extension'] = ''
        expected_response = {
            'photo_extension': ['The photo extension is required'],
        }
        self.abstract_test(data, expected_response, 400)





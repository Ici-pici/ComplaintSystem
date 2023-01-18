from flask_testing import TestCase
from tests.abstract_class import BaseTestClass
from tests.factories import ComplainerFactory
from tests.helper import create_token
from tests.helper import test_photo

class TestComplaintSchema(BaseTestClass):
    URL = '/make_complaint'

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



    def test_title_required(self):
        data = {
            'title': '',
            'description': 'Test description',
            'amount': 10,
            'photo': test_photo,
            'photo_extension': 'png'
        }
        expected_response = {
            'title': ['Title is required.'],
        }
        self.abstract_test(data, expected_response, 400)

    def test_title_too_long(self):
        data = {
            'title': 'aaaaaaaaaaaaaaaaaaaaa',
            'description': 'Test description',
            'amount': 10,
            'photo': test_photo,
            'photo_extension': 'png'
        }
        expected_response = {
            'title': ['The title is too long. 20 Chars max.'],
        }
        self.abstract_test(data, expected_response, 400)

    def test_description_empty_string(self):
        data = {
            'title': 'Test Title',
            'description': '',
            'amount': 10,
            'photo': test_photo,
            'photo_extension': 'png'
        }
        expected_response = {
            'description': ['Description is required.'],
        }
        self.abstract_test(data, expected_response, 400)

    def test_amount_with_negative_number(self):
        data = {
            'title': 'Test Title',
            'description': 'Test Description',
            'amount': -1,
            'photo': test_photo,
            'photo_extension': 'png'
        }
        expected_response = {
            'amount': ['The amount cannot be negative number or zero'],
        }
        self.abstract_test(data, expected_response, 400)

    def test_amount_with_zero(self):
        data = {
            'title': 'Test Title',
            'description': 'Test Description',
            'amount': 0,
            'photo': test_photo,
            'photo_extension': 'png'
        }
        expected_response = {
            'amount': ['The amount cannot be negative number or zero'],
        }
        self.abstract_test(data, expected_response, 400)

    def test_photo_with_empty_string(self):
        data = {
            'title': 'Test Title',
            'description': 'Test Description',
            'amount': 1,
            'photo': '',
            'photo_extension': 'png'
        }
        expected_response = {
            'photo': ['The photo is required'],
        }
        self.abstract_test(data, expected_response, 400)

    def test_photo_extension_with_empty_string(self):
        data = {
            'title': 'Test Title',
            'description': 'Test Description',
            'amount': 1,
            'photo': test_photo,
            'photo_extension': ''
        }
        expected_response = {
            'photo_extension': ['The photo extension is required'],
        }
        self.abstract_test(data, expected_response, 400)





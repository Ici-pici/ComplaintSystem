from flask_testing import TestCase
from db import db
from config import create_app
from tests.factories import ComplainerFactory
from tests.helper import create_token, test_photo, uuid_custom, data_from_transaction
from unittest.mock import patch
from services.s3 import S3Service
from managers.complaint import ComplaintManager
import os
import constants

class TestComplaint(TestCase):
    url = '/make_complaint'

    def create_app(self):
        app = create_app('config.TestsEnv')
        return app

    def setUp(self):
        db.init_app(self.create_app())
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @patch('uuid.uuid4', uuid_custom)
    @patch.object(ComplaintManager, 'issue_transaction', return_value=data_from_transaction)
    @patch.object(S3Service, 'upload', return_value='test_url.bg')
    def test_create_complaint_happy_path(self, s3_mocker, wise_mockup):
        #TODO Make DB tests
        #TODO Make Response text test

        user = ComplainerFactory()
        token = create_token(user)
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        data = {
            'title': 'Test Complaint',
            'description': 'Test description',
            'amount': 10,
            'photo': test_photo,
            'photo_extension': 'png'
        }

        response = self.client.post(self.url, headers=headers, json=data)
        photo_name = f'{uuid_custom()}.{data["photo_extension"]}'
        path = os.path.join(constants.TEMP_FOLDER_PATH, photo_name)
        s3_mocker.assert_called_once_with(path, photo_name)
        wise_mockup.assert_called_once_with(
            amount=data_from_transaction['amount'],
            first_name=user.first_name,
            last_name=user.last_name,
            sort_code=user.sort_code,
            account_number=user.account_number,
            complaint_id=data_from_transaction['complaint_id']
        )

        assert response.status_code == 201


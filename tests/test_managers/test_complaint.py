import os
from unittest.mock import patch

from flask_testing import TestCase

import constants
from config import create_app
from db import db
from managers.complaint import ComplaintManager
from models.complaints import ComplaintModel
from models.enums import StatusEnum
from models.transactions import TransactionModel
from services.s3 import S3Service
from services.wise import WiseService
from tests.factories import ComplainerFactory, ApproverFactory
from tests.helper import create_token, test_photo, uuid_custom, data_from_transaction
from tests.abstract_class import BaseTestClass


class TestComplaint(BaseTestClass):
    URL = '/make_complaint'

    def abstract_test(self, type_user, http_method, url, status_code, data=None):
        if not data:
            data = {}

        # Creating the needed data for the request
        user = type_user()
        token = create_token(user)
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        response = eval(f'self.client.{http_method}("{url}", headers={headers}, json={data})')

        #Check response code
        assert response.status_code == status_code
        return user, response

    @staticmethod
    def db_is_empty_checker():
        # Check if the DB is empty
        complaints = ComplaintModel.query.all()
        assert len(complaints) == 0

        transactions = TransactionModel.query.all()
        assert len(transactions) == 0

    @patch('uuid.uuid4', uuid_custom)
    @patch.object(os, 'remove')
    @patch.object(ComplaintManager, 'issue_transaction', return_value=data_from_transaction)
    @patch.object(S3Service, 'upload', return_value='test_url.bg')
    def test_create_complaint_happy_path(self, s3_mocker, wise_mockup, os_mock):
        data = {
            'title': 'Test Complaint',
            'description': 'Test description',
            'amount': 10,
            'photo': test_photo,
            'photo_extension': 'png',
        }

        self.db_is_empty_checker()

        user, response = self.abstract_test(
            ComplainerFactory,
            'post',
            TestComplaint.URL,
            201,
            data=data
        )

        #Check if it is in DB
        complaints = ComplaintModel.query.all()
        assert len(complaints) == 1

        transactions = TransactionModel.query.all()
        assert len(transactions) == 1

        #Check with mocker objects
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
        os_mock.assert_called_once_with(path)

        #Check response message schema
        expected_response = {
            'photo_url': s3_mocker.return_value,
            'title': data['title'],
            'status': StatusEnum.pending.name,
            'id': user.id,
            'amount': float(data['amount']),
            'description': data['description'],
            'complainer_id': user.id
        }
        assert response.json == expected_response


    @patch('uuid.uuid4', uuid_custom)
    @patch.object(S3Service, 'remove')
    @patch.object(ComplaintManager, 'issue_transaction', return_value=5)
    @patch.object(S3Service, 'upload', return_value='test_url.bg')
    def test_if_the_app_deletes_photos_from_s3_when_catch_exception(
            self,
            s3_upload,
            wize_mock,
            s3_remove
    ):
        data = {
            'title': 'TestTitle',
            'description': 'Test Description',
            'amount': 1,
            'photo': test_photo,
            'photo_extension': 'png'
        }

        self.db_is_empty_checker()
        user, response = self.abstract_test(
            ComplainerFactory,
            'post',
            TestComplaint.URL,
            500,
            data=data
        )

        photo_name = uuid_custom() + f'.{data["photo_extension"]}'
        s3_remove.assert_called_once_with(key=photo_name)
        s3_upload.assert_called()
        wize_mock.assert_called()

        #Check for response
        assert response.json['message'] == 'Something went wrong'


    @patch.object(WiseService, 'fund_transfer')
    def test_approve_method(self, wise_mock):
        self.test_create_complaint_happy_path()
        complaint = ComplaintModel.query.all()[0]
        transaction = TransactionModel.query.all()[0]
        url = f'/complaint/{complaint.id}/approve'

        assert complaint.status == StatusEnum.pending
        approver, response = self.abstract_test(
            ApproverFactory,
            'put',
            url,
            200
        )
        assert complaint.status == StatusEnum.approved
        assert response.json == 204
        wise_mock.assert_called_once_with(transaction.transfer_id)

    @patch.object(WiseService, 'cancel_transfer')
    def test_reject_method(self, wise_mock):
        self.test_create_complaint_happy_path()
        complaint = ComplaintModel.query.all()[0]
        transaction = TransactionModel.query.all()[0]
        url = f'/complaint/{complaint.id}/reject'
        assert complaint.status == StatusEnum.pending
        approver, response = self.abstract_test(
            ApproverFactory,
            'put',
            url,
            200,
        )
        assert complaint.status == StatusEnum.rejected
        wise_mock.assert_called_once_with(transaction.transfer_id)
        assert response.json == 204

    def test_create_complaint_with_unencodable_photo(self):
        data = {
            'title': 'Test Title',
            'description': 'Test Description',
            'amount': 10,
            'photo': 'Some Wrong Photo',
            'photo_extension': 'png'
        }

        user, response = self.abstract_test(
            ComplainerFactory,
            'post',
            TestComplaint.URL,
            400,
            data=data
        )
        assert response.json['message'] == 'Photo decoding failed'




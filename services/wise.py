import requests
from decouple import config
from werkzeug.exceptions import InternalServerError

class WiseService:
    def __init__(self):
        self.token = config('WISE_TOKEN')
        self.main_url = config("MAIN_URL")
        self.headers = {
            'Authorization': f'Bearer {config("WISE_TOKEN")}',
            'Content-Type': 'application/json'
        }
        self.error_message = 'The payment provider is not available'
        self.profile_id = self._get_profile_id()

    def _get_profile_id(self):
        url = f'{self.main_url}/v1/profiles'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return [x['id'] for x in response.json() if x['type'] == 'personal'][0]
        else:
            raise InternalServerError(self.error_message)

    def create_quote(self, source_currency, target_currency, target_amount):
        url = f'{self.main_url}/v2/quotes'
        # url = f'{self.main_url}/v3/profiles/{self.profile_id}/quotes'
        data = {
            "sourceCurrency": source_currency,
            "targetCurrency": target_currency,
            "targetAmount": target_amount,
            # "targetAmount": null,
            "profile": self.profile_id
        }
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 200:
            return response.json()['id']
        else:
            raise InternalServerError(self.error_message)

    def create_recipient(self, currency, first_name, last_name, sort_code, account_number):
        url = f'{self.main_url}/v1/accounts'
        data = {
            "currency": currency,
            "type": "sort_code",
            "profile": self.profile_id,
            "accountHolderName": f"{first_name} {last_name}",
            "legalType": "PRIVATE",
            "details": {
                "sortCode": sort_code,
                "accountNumber": account_number
            }
        }
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 200:
            return response.json()['id']
        else:
            raise InternalServerError(self.error_message)

    def create_transfer(self, target_id, quot_id, customer_uuid):
        url = f'{self.main_url}/v1/transfers'
        data = {
            "targetAccount": target_id,
            "quoteUuid": quot_id,
            "customerTransactionId": customer_uuid,
            "details": {
                "reference": "to my friend",
                "transferPurpose": "verification.transfers.purpose.pay.bills",
                "sourceOfFunds": "verification.source.of.funds.other"
            }
        }
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 200:
            return response.json()['id']
        else:
            raise InternalServerError(self.error_message)


    def fund_transfer(self, transfer_id):
        url = f'{self.main_url}/v3/profiles/{self.profile_id}/transfers/{transfer_id}/payments'
        data = {'type': 'BALANCE'}
        response = requests.post(url, headers=self.headers, json=data)
        if not response.status_code == 201:
            raise InternalServerError(self.error_message)


    def cancel_transfer(self, transfer_id):
        url = f'{self.main_url}/v1/transfers/{transfer_id}/cancel'
        response = requests.put(url, headers=self.headers)
        if not response.status_code == 200:
            raise InternalServerError(self.error_message)



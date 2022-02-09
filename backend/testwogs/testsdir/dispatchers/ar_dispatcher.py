"""
    AgencyRegister
"""
from testwogs.testsdir.classes.http_client import Client
from testwogs.testsdir.classes.log_manager import LogManager


class AgencyRegisterDispatcher:
    def __init__(self, domain_name, account, token):
        self.method = 'POST'
        self.request_url = 'account/register/agency'
        self.domain_name = domain_name
        self.account = account
        self.token = token
        self.client = Client()
        self.log_manager = LogManager()

    def do(self):
        import random
        num = random.randint(100, 700)
        email = f'emiltest{num}@gmail.com'
        data_request = {
            "name": "Agency1",
            "director": "Boss1",
            "address": "Kiev1",
            "payment_method": "visa",
            "contact_email": "agency1@gmail.com",
            "skype": "agency1-skype",
            "other_messanger": "Viber",
            "country": "USA",
            "city": "Ny",
            "email": email,
            "phone1": "25534554",
            "phone2": "34535345",
            "images": "[]"
            }
        rec = self.client.post_json(self.domain_name + self.request_url, data_request, token=self.token)
        if rec.status_code == 200:
            # truncate data, save data in DB
            self.log_manager.truncate_db()
            self.log_manager.add(rec.status_code, self.request_url, request='', response=rec.text,
                                 alias='register_agency', method=self.method)

            # information output to the console
            print('=' * 50)
            print(f'URL_REQUEST - {self.request_url}\nRegister agency test completion\n'
                  f'status - {rec.status_code} - Ok')
            print('=' * 50)
        else:
            # truncate data, save data in DB
            self.log_manager.truncate_db()
            self.log_manager.add(rec.status_code, self.request_url, request='',
                                 response=rec.text, test_status='no successfully',
                                 api_status=1, alias='register_agency', method=self.method)
            # information output to the console
            print('=' * 50)
            print(f'Something is wrong.\nURL_REQUEST - {self.request_url}\nTest completion status - {rec.status_code}')
            print('=' * 50)
            return False
"""
    Login Dispatcher - user login
"""
import json
from testwogs.testsdir.classes.http_client import Client
from testwogs.testsdir.classes.log_manager import LogManager

class LoginDispatcher:

    def __init__(self, domain_name, account):
        self.method = 'POST'
        self.request_url = 'api-token-auth/'
        self.domain_name = domain_name
        self.account = account
        self.client = Client()
        self.log_manager = LogManager()

    def do(self):
        data_request = {'username': self.account['login'], 'password': self.account['password']}
        rec = self.client.post_json(self.domain_name + self.request_url, data_request)
        if rec.status_code == 200:
            # truncate data, save data in DB
            self.log_manager.truncate_db()
            self.log_manager.add(rec.status_code, self.request_url, json.dumps(data_request), rec.text,
                                 alias='login', method=self.method)

            # information output to the console
            print('=' * 50)
            print(f'URL_REQUEST - {self.request_url}\nLogintest completion status - {rec.status_code} - Ok')
            print('=' * 50)
            return rec.json()['token']
        else:
            # truncate data, save data in DB
            self.log_manager.truncate_db()
            self.log_manager.add(rec.status_code, self.request_url, json.dumps(data_request),
                                 rec.text, test_status='no successfully',
                                 api_status=1, alias='login', method=self.method)
            # information output to the console
            print('=' * 50)
            print(f'Something is wrongs.\nURL_REQUEST - {self.request_url}\nTest completion status - {rec.status_code}')
            print('=' * 50)
            return False
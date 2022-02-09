""""
   Logout Dispatcher- Logout class
"""
import json
from testwogs.testsdir.classes.http_client import Client
from testwogs.testsdir.classes.log_manager import LogManager


class LogoutDispatcher:
    def __init__(self, domain_name, account, token):
        self.method = 'GET'
        self.request_url = 'logout/'
        self.domain_name = domain_name
        self.account = account
        self.token = token
        self.client = Client()
        self.log_manager = LogManager()

    def do(self):
        rec = self.client.get_json(self.domain_name + self.request_url, token=self.token)
        if rec.status_code == 200:
            # truncate data, save data in DB
            self.log_manager.truncate_db()
            self.log_manager.add(rec.status_code, self.request_url, json.dumps(rec.text), api_status=1,
                                 alias='logout', method=self.method)
            # information output to the console
            print('=' * 50)
            print(f'URL_REQUEST - {self.request_url}\nLogoutTest completion status - {rec.status_code} - Ok')
            print('=' * 50)
        else:
            # truncate data, save data in DB
            self.log_manager.truncate_db()
            self.log_manager.add(rec.status_code, self.request_url, json.dumps(rec.text), api_status=1,
                                 alias='logout', test_status='no successfully', method=self.method)
            # information output to the console
            print('=' * 50)
            print(f'Something is wrong.\nURL_REQUEST - {self.request_url}\n'
                  f'LogoutTest completion status - {rec.status_code}')
            print('=' * 50)
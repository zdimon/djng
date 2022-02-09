"""
    Online Dispatcher - get users online
"""
import json
from testwogs.testsdir.classes.http_client import Client
from testwogs.testsdir.classes.log_manager import LogManager


class OnlineDispatcher:
    def __init__(self, domain_name, account, token):
        self.method = 'GET'
        self.request_url = 'online/count'
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
            self.log_manager.add(rec.status_code, self.request_url, request='', response=rec.text,
                                 alias='online_count', method=self.method)

            # information output to the console
            print('=' * 50)
            print(f'URL_REQUEST - {self.request_url}\nOnlinetest completion status - {rec.status_code} - Ok')
            print('=' * 50, 888)
        else:
            # truncate data, save data in DB
            self.log_manager.truncate_db()
            self.log_manager.add(rec.status_code, self.request_url, request='',
                                 response=rec.text, test_status='no successfully',
                                 api_status=1, alias='online_count', method=self.method)
            # information output to the console
            print('=' * 50)
            print(f'Something is wrong.\nURL_REQUEST - {self.request_url}\nTest completion status - {rec.status_code}')
            print('=' * 50)
            return False
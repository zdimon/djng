"""
    Update socket Online Dispatcher - set users sockt id
"""
from testwogs.testsdir.classes.http_client import Client
from testwogs.testsdir.classes.log_manager import LogManager


class OnlineSocketDispatcher:
    def __init__(self, domain_name, account, token):
        self.method = 'POST'
        self.request_url = 'online/update/socket/id'
        self.domain_name = domain_name
        self.account = account
        self.token = token
        self.client = Client()
        self.log_manager = LogManager()

    def do(self):
        data_request = {'token': self.token, 'socket_id': 1}
        rec = self.client.post_json(self.domain_name + self.request_url, data_request, token=self.token)
        if rec.status_code == 200:
            # truncate data, save data in DB
            self.log_manager.truncate_db()
            self.log_manager.add(rec.status_code, self.request_url, request='', response=rec.text,
                                 alias='online_socket', method=self.method)

            # information output to the console
            print('=' * 50)
            print(f'URL_REQUEST - {self.request_url}\nOnline socket update test completion '
                  f'status - {rec.status_code} - Ok')
            print('=' * 50)
        else:
            # truncate data, save data in DB
            self.log_manager.truncate_db()
            self.log_manager.add(rec.status_code, self.request_url, request='',
                                 response=rec.text, test_status='no successfully',
                                 api_status=1, alias='online/update/socket/id', method=self.method)
            # information output to the console
            print('=' * 50)
            print(f'Something is wrong.\nURL_REQUEST - {self.request_url}\nTest completion status - {rec.status_code}')
            print('=' * 50)
            return False
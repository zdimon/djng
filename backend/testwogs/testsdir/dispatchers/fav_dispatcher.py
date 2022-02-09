""""
   Favorite Dispatcher Class
"""

import json
from testwogs.testsdir.classes.http_client import Client
from testwogs.testsdir.classes.log_manager import LogManager

class FavDispatcher:
    def __init__(self, domain_name, account, token):
        self.method = 'GET'
        self.request_url = 'account/favorites'
        self.domain_name = domain_name
        self.account = account
        self.token = token
        self.client = Client()
        self.log_manager = LogManager()
        self.limit = 5
        self.offset = 2

    def do(self):
        data_request = {'limit': self.limit, 'offset': self.offset}
        rec = self.client.get_json(self.domain_name + self.request_url, data_request, token=self.token)

        if rec.status_code == 200:
            # truncate data, save data in DB
            self.log_manager.truncate_db()
            self.log_manager.add(rec.status_code, self.request_url, json.dumps(data_request), json.dumps(rec.text),
                                 alias='favorites', method=self.method)
            # information output to the console
            print('=' * 50, 788)
            print(f'URL_REQUEST - {self.request_url}\nFavoritesTest completion status - {rec.status_code} - Ok')
            print('=' * 50)
        else:
            # truncate data, save data in DB
            self.log_manager.truncate_db()
            self.log_manager.add(rec.status_code, self.request_url, json.dumps(rec.text),
                                 test_status='no successfully', api_status=1, alias='favorites',
                                 method=self.method)
            # information output to the console
            print('=' * 50)
            print(f'URL_REQUEST - {self.request_url}\n'
                  f'Something is wrong!!!\nFavoritesTest completion status - {rec.status_code}')
            print('=' * 50)
"""
   Server Request Class to urls REST API
"""

import requests
import sys
from .log_manager import LogManager

class Client:

    def __init__(self):
        self.header = {'Content-Type': 'application/json'}

    def post_json(self, url, data_request, token=None):
        
        if token:
            headers = {'Content-Type': 'application/json', 'Authorization': 'Token ' + token}
        else:
            headers = self.header
        try:
            return requests.post(url, json=data_request, headers=headers)
        except Exception as e:
            print('Server does not respond!!!', e)
            LogManager.server_error()
            sys.exit()
            
    def get_json(self, url, data_request='', headers='', token=''):
        headers = {'Content-Type': 'application/json', 'Authorization': 'Token ' + token}
        try:
            return requests.get(url, json=data_request, headers=headers)
        except Exception as e:
            print('Server does not respond!!!!', e)
            LogManager.server_error()
            sys.exit()

    def put_json(self):
        pass

    def delete_json(self):
        pass
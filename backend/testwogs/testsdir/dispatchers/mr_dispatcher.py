"""
    ManRegisterDispatcher
"""
from testwogs.testsdir.classes.http_client import Client
from testwogs.testsdir.classes.log_manager import LogManager


class ManRegisterDispatcher:
    def __init__(self, domain_name, account, token):
        self.method = 'POST'
        self.request_url = 'account/register/man'
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
          "name": "TestName",
          "about_me": "Test me",
          "language": "ru",
          "gender": "male",
          "email": email,
          "goal": "found something",
          "job": "slesar",
          "city": "Kiev",
          "lookingfor": "men",
          "birthday": "2013-10-10",
          "images": []
        }
        rec = self.client.post_json(self.domain_name + self.request_url, data_request, token=self.token)
        if rec.status_code == 200:
            # truncate data, save data in DB
            self.log_manager.truncate_db()
            self.log_manager.add(rec.status_code, self.request_url, request='', response=rec.text,
                                 alias='register_man', method=self.method)

            # information output to the console
            print('=' * 50)
            print(f'URL_REQUEST - {self.request_url}\nRegister man test completion\n'
                  f'status - {rec.status_code} - Ok')
            print('=' * 50)
        else:
            # truncate data, save data in DB
            self.log_manager.truncate_db()
            self.log_manager.add(rec.status_code, self.request_url, request='',
                                 response=rec.text, test_status='no successfully',
                                 api_status=1, alias='register_man', method=self.method)
            # information output to the console
            print('=' * 50)
            print(f'Something is wrong.\nURL_REQUEST - {self.request_url}\nTest completion status - {rec.status_code}')
            print('=' * 50)
            return False
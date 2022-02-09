"""
    Test Logging Class
"""
from testwogs.models import Logserver

class LogManager:

    def add(self, server_status, url_request, request='', response='', test_status='successfully',
            alias='No message', api_status=0, method=''):

        Logserver.objects.save_new_record(server_status, url_request, request, response, test_status, alias,
                                          api_status, method)

    def truncate_db(self):
        data = Logserver.objects.all()
        data.delete()

    @staticmethod
    def server_error():
        Logserver.objects.save_new_record(500, 'index', '', '', 1, 'not-response', 1)
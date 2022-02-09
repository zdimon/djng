
from django.core.management.base import BaseCommand, CommandError

from backend import settings as main_settings
from testwogs import settings
from testwogs.testsocket.client_socket import ClientSocket
from testwogs.models import Logserver

class BaseTestCommand(BaseCommand):

    def __init__(self):
        self.domain = main_settings.TESTS_DEFAULT['default_url']
        self.default_account = main_settings.TESTS_DEFAULT['default_account']

    def add_arguments(self, parser):
        parser.add_argument('test_name', nargs='?', default='False', type=str)
        parser.add_argument('domain_name', nargs='?', default='False', type=str)
        parser.add_argument('account', nargs='?', default='False', type=str)

    def handle(self, *args, **options):
        print('Init base test class')
        print('Test domain %s' % self.domain)
        print('Clear DB')
        Logserver.objects.all().delete()

    # def handle(self, *args, **options):
    #     if options['test_name'] == 'help':
    #         self.help_runtest()
    #         return

    #     if options['test_name'] == 'showtests':
    #         self.show_all_tests()
    #         return

    #     """
    #         Get domain and account 
    #     """
    #     def_domain, def_account = self.set_data_request(options)

    #     """
    #        Run all tests
    #     """

    #     if options['test_name'] == 'runall':
    #         self.run_all_tests(def_domain, def_account)
    #         return
    #     """
    #         Run single test
    #     """
    #     try:
    #         test_object = settings.TESTS_DICT[options['test_name']]['class_name']
    #         test_object.run_test(def_domain, def_account)
    #     except KeyError as key:
    #         print(f'Wrong test names - {key}!!!')

    #     """
    #         Sockets test
    #     """
    #     if options['test_name'] == 'clientsocket':
    #         siO = ClientSocket()
    #         siO.run_server()
    #         return
    #     self.stdout.write(self.style.SUCCESS('The program is completed!'))

    # def run_all_tests(self, domain_name, account):
    #     try:
    #         for name in settings.TESTS_DICT:
    #             test_object = settings.TESTS_DICT[name]['class_name']
    #             test_object.run_test(domain_name, account)
    #     except KeyError as key:
    #         print(f'Wrong test name - {key}!!!')

    # def show_all_tests(self):
    #     for test in settings.TESTS_DICT:
    #         print(test)

    def help_runtest(self):
        print('Command to show all name tests - manage.py runtest showtests\n')
        print('Command to run single test - manage.py runtest <test_name> <domain_name> <account>\n')
        print('Command to run all tests - manage.py runtest runall <domain_name> <account>\n')
        print('Domains to choose - local, dev, prod. Default domain - local\n')
        print('Accounts to choose - man, woman. Default domain - man')

    # """
    #     Setting values for domain and account
    # """

    # def set_data_request(self, options) -> tuple:
    #     if options['domain_name'] != 'False' and options['domain_name'] in main_settings.TESTS_DOMAINS:
    #         def_domain = main_settings.TESTS_DOMAINS[options['domain_name']]
    #     else:
    #         def_domain = main_settings.TESTS_DEFAULT['default_url']

    #     if options['account'] != 'False' and options['account'] in main_settings.TESTS_ACCOUNTS:
    #         def_account = main_settings.TESTS_ACCOUNTS[options['account']]
    #     else:
    #         def_account = main_settings.TESTS_DEFAULT['default_account']
    #     # print(def_domain, def_account)
    #     return def_domain, def_account
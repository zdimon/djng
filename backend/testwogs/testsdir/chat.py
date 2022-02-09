""""
    LoginTest - Login class
"""

from testwogs.testsdir.intertests import BaseTests
from testwogs.testsdir.classes.user_class import User


class ChatTest(BaseTests):

    def run_test(self, domain_name, account):
        print('Chat test')
        user = User(domain_name, account)
        #user.do_login()
        user.socket_connect()
        return True
""""
    WomanRegisterTest class
    Register woman account
"""

from testwogs.testsdir.intertests import BaseTests
from testwogs.testsdir.classes.user_class import User


class WomanRegisterTest(BaseTests):
    def run_test(self, domain_name, account):
        user = User(domain_name, account)
        user.do_woman_register()
""""
    Online Update Socket id Test - update socket
"""

from testwogs.testsdir.intertests import BaseTests
from testwogs.testsdir.classes.user_class import User


class UpdateSocketTest(BaseTests):

    def run_test(self, domain_name, account):
        user = User(domain_name, account)
        user.update_socket_online()
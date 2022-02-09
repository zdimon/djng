""""
    Online List Test - return list of online users
"""

from testwogs.testsdir.intertests import BaseTests
from testwogs.testsdir.classes.user_class import User


class ListOnlineTest(BaseTests):

    def run_test(self, domain_name, account):
        user = User(domain_name, account)
        user.get_online_list()
""""
    Online Count Test - return count of online users
"""

from testwogs.testsdir.intertests import BaseTests
from testwogs.testsdir.classes.user_class import User


class OnlineTest(BaseTests):

    def run_test(self, domain_name, account):
        user = User(domain_name, account)
        user.get_online_count()

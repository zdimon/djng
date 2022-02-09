""""
    FavoritesTest class
    Pre-receives the user token
"""

from testwogs.testsdir.intertests import BaseTests
from testwogs.testsdir.classes.user_class import User


class FavoritesTest(BaseTests):
    def run_test(self, domain_name, account):
        user = User(domain_name, account)
        user.do_favorite()
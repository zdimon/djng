""""
    AgencyRegisterTest class
    Register agency account
"""

from testwogs.testsdir.intertests import BaseTests
from testwogs.testsdir.classes.user_class import User


class AgencyRegisterTest(BaseTests):
    def run_test(self, domain_name, account):
        user = User(domain_name, account)
        user.do_agency_register()
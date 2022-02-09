from testwogs.testsdir.login import LoginTest
from testwogs.testsdir.logouttest import LogoutTest
from testwogs.testsdir.favoritestest import FavoritesTest
from testwogs.testsdir.online_count import OnlineTest
from testwogs.testsdir.online_list import ListOnlineTest
from testwogs.testsdir.online_socket import UpdateSocketTest
from testwogs.testsdir.woman_register import WomanRegisterTest
from testwogs.testsdir.man_register import ManRegisterTest
from testwogs.testsdir.agency_register import AgencyRegisterTest


"""
    Base URL API
"""
BASE_URL_API = 'https://ng-dating-test.webmonstr.com/'

"""
    User Defaults Settings
"""
USER_NAME = 'admin'
USER_PASSWORD = 'admin'
USER_EMAIL = 'admin@do.com'

"""
    Tests dict
"""
TESTS_DICT = {
    'login': {'class_name': LoginTest(), 'request_url': 'api-token-auth/', 'method': 'POST'},
    'logout': {'class_name': LogoutTest(), 'request_url': 'logout/', 'method': 'GET'},
    'favorites': {'class_name': FavoritesTest(), 'request_url': 'account/favorites', 'method': 'GET'},
    'online_count': {'class_name': OnlineTest(), 'request_url': 'online/count', 'method': 'GET'},
    'online_list': {'class_name': ListOnlineTest(), 'request_url': 'online/list', 'method': 'GET'},
    'online_socket': {'class_name': UpdateSocketTest(), 'request_url': 'online/update/socket/id', 'method': 'POST'},
    'register_woman': {'class_name': WomanRegisterTest(), 'request_url': 'account/register/woman', 'method': 'POST'},
    'register_man': {'class_name': ManRegisterTest(), 'request_url': 'account/register/man', 'method': 'POST'},
    'register_agency': {'class_name': AgencyRegisterTest(), 'request_url': 'account/register/agency', 'method': 'POST'},
}

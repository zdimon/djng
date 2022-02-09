"""
    User class.
    Сontains methods appropriate REST API url's
"""

import sys
import json
from testwogs.testsdir.dispatchers.login_dispatcher import LoginDispatcher
from testwogs.testsdir.dispatchers.logout_dispatcher import LogoutDispatcher
from testwogs.testsdir.dispatchers.online_dispatcher_count import OnlineDispatcher
from testwogs.testsdir.dispatchers.online_dispatcher_list import OnlineListDispatcher
from testwogs.testsdir.dispatchers.fav_dispatcher import FavDispatcher
from testwogs.testsdir.dispatchers.online_dispatcher_socket import OnlineSocketDispatcher
from testwogs.testsdir.socket.client_socket import ClientSocket
from testwogs.testsdir.dispatchers.wr_dispatcher import WomanRegisterDispatcher
from testwogs.testsdir.dispatchers.mr_dispatcher import ManRegisterDispatcher
from testwogs.testsdir.dispatchers.ar_dispatcher import AgencyRegisterDispatcher

class User:

    def __init__(self, domain_name, account):
        self.account = account
        self.domain_name = domain_name
        self.token = self.set_token()
        self.socket_client = ClientSocket()

    def set_token(self):
        self.token = self.do_login()
        if not self.token:
            print('User have not token!!!')
            sys.exit()
        return self.token

    def do_login(self):
        dispatcher = LoginDispatcher(self.domain_name, self.account)
        self.token = dispatcher.do()
        return self.token

    def do_logout(self):
        dispatcher = LogoutDispatcher(self.domain_name, self.account, self.token)
        dispatcher.do()

    def do_favorite(self):
        dispatcher = FavDispatcher(self.domain_name, self.account, self.token)
        dispatcher.do()

    def get_online_count(self):
        dispatcher = OnlineDispatcher(self.domain_name, self.account, self.token)
        dispatcher.do()

    def get_online_list(self):
        dispatcher = OnlineListDispatcher(self.domain_name, self.account, self.token)
        dispatcher.do()

    def update_socket_online(self):
        dispatcher = OnlineSocketDispatcher(self.domain_name, self.account, self.token)
        dispatcher.do()

    def do_woman_register(self):
        dispatcher = WomanRegisterDispatcher(self.domain_name, self.account, self.token)
        dispatcher.do()

    def do_man_register(self):
        dispatcher = ManRegisterDispatcher(self.domain_name, self.account, self.token)
        dispatcher.do()

    def do_agency_register(self):
        dispatcher = AgencyRegisterDispatcher(self.domain_name, self.account, self.token)
        dispatcher.do()

    def set_sid(self,res):
        dat = json.loads(res.text)
        try:
            self.token = dat['token']
        except:
            self.token = None
        print(self.token)

    def send_chat_message(sid,room,message):
        pass

    def get_chat_rooms(self):
        pass

    def get_main_page(self):
        pass

    def add_like(user):
        pass

    def subscribe(user):
        pass

    def send_comment(feed):
        pass

    def add_photo(photo):
        pass

    def socket_connect(self):
        if not self.token:
            self.do_login()
        self.socket_client.run_server()

from django.core.management.base import BaseCommand, CommandError

from backend import settings as main_settings
from testwogs import settings
from testwogs.testsocket.client_socket import ClientSocket
from testwogs.management.commands.base import BaseTestCommand
from testwogs.testsdir.classes.user_class import User

class Command(BaseTestCommand):


    def handle(self, *args, **options):
        super(Command,self).handle()
        account = {
            "login": "man1@gmail.com",
            "password": "man1"
        }
        man = User(self.domain, account)
        man.do_login()
        man.socket_connect()




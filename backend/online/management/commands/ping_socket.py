from django.core.management.base import BaseCommand, CommandError
from online.tasks import ping_socket, clear_offline

class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Ping')
        ping_socket()
        #clear_offline()
from django.core.management.base import BaseCommand, CommandError
from online.tasks import ping_socket, clear_offline, update_online

class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Ping')
        update_online()
        #clear_offline()
from django.core.management.base import BaseCommand, CommandError
from online.tasks import ping_socket, clear_offline
import time
class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Ping')
        #ping_socket()
        #time.sleep(2)
        clear_offline()
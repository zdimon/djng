from django.core.management.base import BaseCommand, CommandError
from online.tasks import ping_socket, remove_offline
import time
class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Removing offline')
        remove_offline()
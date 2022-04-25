from django.core.management.base import BaseCommand, CommandError
import requests
from backend.settings import DOMAIN

class Command(BaseCommand):
    'Test offline'
    help = 'Test offline'
    def handle(self, *args, **options):
        url = '%s/celery/task' % DOMAIN
        data = {'task': 'user_offline', 'username': 'admin'}
        res = requests.post(url,data=data)
        print(res.text)
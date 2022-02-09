from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from backend.settings import DOMAIN, BASE_DIR
from django.core.files import File
from webmaster.models import Webmaster
from account.models import UserProfile
from django.contrib.auth.models import Group



class Command(BaseCommand):
    'Import webmasters into DB'
    def handle(self, *args, **options):
        print('Importing webmasters into DB...')
        Webmaster.objects.all().delete()
        a = Webmaster()
        a.username = 'webmaster1'
        a.name = 'webmaster1'
        a.login = 'webmaster1'
        a.adress = 'kutuzova 7'
        a.city = 'Kherson'
        a.contact_email = 'svaha@gmail.com'
        a.set_password('webmaster1')
        a.save()
        my_group = Group.objects.get(name='webmaster') 
        my_group.user_set.add(a)


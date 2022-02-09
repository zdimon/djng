from django.core.management.base import BaseCommand, CommandError
from account.models import UserProfile
#from photo.models import UserPhoto
from administration.models import AdminProfile
from django.contrib.auth.models import User
from backend.settings import DOMAIN, BASE_DIR
from django.core.files import File
import random
from django.utils.dateparse import parse_date
from django.contrib.auth.models import Group
from account.models import UserProfile



def create_users():
    print('Creating....admin')
    #country = random.choice(COUNTRIES.keys())
    u = UserProfile()
    u.username = 'admin'
    u.set_password('admin')
    u.is_active = True
    u.is_staff = True
    u.is_superuser = True
    u.email = '%s@gmail.com' % 'admin'
    u.is_superuser = True
    u.gender = 'male'
    u.save()
    my_group = Group.objects.get(name='admin') 
    my_group.user_set.add(u)
    my_group = Group.objects.get(name='director') 
    my_group.user_set.add(u)
    my_group = Group.objects.get(name='manager') 
    my_group.user_set.add(u)
    my_group = Group.objects.get(name='moderator') 
    my_group.user_set.add(u)
    my_group = Group.objects.get(name='webmaster') 
    my_group.user_set.add(u)

    u = AdminProfile()
    u.username = 'moderator'
    u.set_password('moderator')
    u.is_active = True
    u.is_staff = True
    u.is_superuser = True
    u.email = '%s@gmail.com' % 'moderator'
    u.is_superuser = False
    u.save()
    my_group = Group.objects.get(name='moderator') 
    my_group.user_set.add(u)

    return u

class Command(BaseCommand):
    'Import administrations into DB'
    def handle(self, *args, **options):
        print('Importing admin users...')
        AdminProfile.objects.all().delete()
        create_users()
        
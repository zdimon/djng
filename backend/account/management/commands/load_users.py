from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

class Command(BaseCommand):
    'Import test users into DB'
    help = 'Import test users into DB'
    def handle(self, *args, **options):
        print('Importing users...')
        User.objects.all().delete()
        user = User()
        user.set_password('admin')
        user.username = 'admin'
        user.is_active = True
        user.is_superuser = True
        user.save()
        for i in range(1,10):
            user = User()
            user.set_password('user%s' % i)
            user.username = 'user%s' % i
            user.is_active = True
            user.is_superuser = True
            user.save()            
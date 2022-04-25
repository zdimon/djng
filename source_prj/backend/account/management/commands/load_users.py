from django.core.management.base import BaseCommand, CommandError
from account.models import UserProfile
#from photo.models import UserPhoto
from usermedia.models import UserMedia
from django.contrib.auth.models import User
from backend.settings import DOMAIN, BASE_DIR
from django.core.files import File
import random
from django.utils.dateparse import parse_date

SITIES = [
    'Kherson',
    'Nikolaev',
    'Odessa',
    'Kahovka',
    'Kiev',
    'Melitopol',
    'Dnepr',
    'Lviv'
]

from django_countries.data import COUNTRIES

def load_photo(userprofile,number):
    '''
    Import photos from test_data/images
    '''
    print('Loading...%s' % userprofile)
    p = UserMedia()
    p.user = userprofile
    p.is_approved = True
    p.is_main = True
    if userprofile.gender == 'male':
        filepath = BASE_DIR+'/test_data/images/m%s.jpeg' % number
    else:
        filepath = BASE_DIR+'/test_data/images/w%s.jpeg' % number
    with open(filepath, 'rb') as image:
        p.image.save('%s.jpeg'% userprofile.id, File(image), save=True)
    p.save()

def users_fabric(name,gender,is_superuser):
        '''
        Fabric to create user`s objects and save it into DB
        '''
        print('Creating....%s' % name)
        #country = random.choice(COUNTRIES.keys())
        i = random.randint(0, len(COUNTRIES) - 1)
        country = list(COUNTRIES)[i]
        i = random.randint(0, len(SITIES) - 1)
        city = SITIES[i]

        u = UserProfile()
        u.username = '%s@gmail.com' % name
        u.country = country
        u.city = city
        u.publicname = 'p'+name
        u.gender = gender
        u.set_password(name)
        u.is_active = True
        u.is_staff = True
        u.email = '%s@gmail.com' % name
        u.is_superuser = is_superuser
        u.about_me = 'I am %s' % ' from %s' % city
        bd = '19%s-%s-01' % (random.randint(76,99),random.randint(1,12))
        u.birthday = parse_date(bd)
        u.hight = 160
        u.save()
        return u

class Command(BaseCommand):
    'Import test users into DB'
    help = 'Import test users into DB'
    def handle(self, *args, **options):
        print('Importing users...')
        UserProfile.objects.all().delete()

        #load_photo(admin,1)
        for i in range(1,20):
            name = 'man%s' % i
            profile = users_fabric(name,'male',False)
            #load_photo(profile,i)
        for i in range(1,20):
            name = 'woman%s' % i
            profile = users_fabric(name,'female',False)
            #load_photo(profile,i)

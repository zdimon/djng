from django.core.management.base import BaseCommand, CommandError
from props.models import Props, Value, Value2User

from .utils import load_props
from django_countries.data import COUNTRIES
from backend.settings import BASE_DIR
import json
from account.models import UserProfile
from django.core.files import File

def seed_users():
    for u in UserProfile.objects.filter(gender='female'):
        print('seeding .... %s' % u)
        for p in Props.objects.filter(for_woman=True, type='one'):
            v = Value.objects.filter(prop=p).order_by('?').first()
            u2v = Value2User()
            u2v.prop = p
            u2v.value = v
            u2v.user = u
            u2v.save()


def insert_one(d):
    print('Saving....%s' % d['name_en'])
    source_dir = BASE_DIR+'/test_data/icons/Personal_info'
    im = source_dir+'/%s' % d['icon']
    print('Save icon %s' % im)
    p = Props()
    p.name_ru = d['name_ru']
    p.name_en = d['name_en']
    p.alias = d['alias']
    p.type = d['type']
    p.category = d['category']
    p.for_woman = True
    with open(im, 'rb') as image:
        p.icon.save(d['icon'], File(image), save=True)
    p.save()
    try:
        for i in d['options']:
            source_dir = BASE_DIR+'/test_data/icons/Personal_info'
            im = source_dir+'/%s' % i['icon']
            v = Value()
            v.prop = p
            v.name_ru = i['name_ru']
            v.name_en = i['name_en']
            with open(im, 'rb') as image:
                v.icon.save(i['icon'], File(image), save=True)
            v.save()
    except Exception as e:
        print('No options for %s' % d['name_ru'])

    
class Command(BaseCommand):
    'Import props into DB'
    help = 'Import props into DB'

    def handle(self, *args, **options):
        print('Importing props...')
        Props.objects.all().delete()
        Value.objects.all().delete()

        path = BASE_DIR+'/test_data/props.json'
        with open(path,'r') as f:
            data = f.read()
            jdata = json.loads(data)
        
        for i in jdata:
            insert_one(i)
        seed_users()



        '''
        load_props()


        prop = Props.objects.create(name="Country", name_ru="Country", alias="сountry", for_woman=True)

        for value in COUNTRIES.values():
            Value.objects.bulk_create([
                Value(prop=prop, name=value, name_ru=value)
            ])
            print('Prop %s created!' % value)
        print('All props are loaded!')
        '''

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from backend.settings import DOMAIN, BASE_DIR
from django.core.files import File
import random
from django.utils.dateparse import parse_date
from menu.models import Menu, Menu2User
# https://keenthemes.com/metronic/preview/demo1/components/icons/flaticon.html

MENU = [
    {"name": "log", "title": "Activity log", "icon": "flaticon-questions-circular-button", "page": "/log/list"},
    {"name": "payment", "title": "Payments", "icon": "flaticon-list", "page": "/payment/list"},
    {"name": "payment_type", "title": "Payment types", "icon": "flaticon-cogwheel-1", "page": "/payment/type"},
    {"name": "user", "title": "Users", "icon": "flaticon-avatar", "page": "/user/list"},
    {"name": "moderation", "title": "Moderation", "icon": "flaticon2-expand", "page": "/moderation/list"},
    {"name": "plan", "title": "Plans", "icon": "flaticon2-expand", "page": "/plan/list"}
]

class Command(BaseCommand):
    'Load menu into DB'
    help = 'Import test menu into DB'
    def handle(self, *args, **options):
        print('Importing menu...')
        Menu.objects.all().delete()
        Menu2User.objects.all().delete()
        for i in MENU:
            m = Menu()
            m.name = i['name']
            m.title = i['title']
            m.icon = i['icon']
            m.page = i['page']
            m.save()
            print('Creating menu...%s' % i['title'])

            u = User.objects.get(username='admin')
            m2u = Menu2User()
            m2u.user = u
            m2u.menu = m
            m2u.save()

            try:
                u = User.objects.get(username='agency-director-agency1')
                m2u = Menu2User()
                m2u.user = u
                m2u.menu = m
                m2u.save()

                u = User.objects.get(username='agency-manager-agency1')
                m2u = Menu2User()
                m2u.user = u
                m2u.menu = m
                m2u.save()

                u = User.objects.get(username='webmaster1')
                m2u = Menu2User()
                m2u.user = u
                m2u.menu = m
                m2u.save()

                u = User.objects.get(username='moderator')
                m2u = Menu2User()
                m2u.user = u
                m2u.menu = m
                m2u.save()
            except:
                pass
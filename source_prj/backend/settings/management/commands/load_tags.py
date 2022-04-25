from django.core.management.base import BaseCommand, CommandError
from settings.models import AppSettings, Pictures, ReplanishmentPlan
from backend.settings import BASE_DIR
from account.models import UserProfile
from props.models import Props, Value, Value2User
import json
from feed.models import UserFeed



def load_tags_to_profile():
    print('Load tags')
    for p in UserProfile.objects.all():
        print('User %s' % p.username)
        p.tags.clear()
        p.tags.add(str(p.id), p.gender, p.publicname, p.zodiac, p.city, p.get_country_display())
        for v in Value2User.objects.filter(user = p):
            p.tags.add(v.value.name)

def load_feed_tags():
    print('Load tags')
    for p in UserFeed.objects.all():
        print('Feed %s' % p.id)
        p.tags.clear()
        p.tags.add(str(p.city), p.country)
        

class Command(BaseCommand):
    'Import tags'
    help = 'Import tags'


    def handle(self, *args, **options):
        load_tags_to_profile()
        load_feed_tags()
      
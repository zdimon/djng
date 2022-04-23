from django.core.management.base import BaseCommand, CommandError
from account.models import UserProfile
from backend.settings import DOMAIN, BASE_DIR
import requests
import sys
import json
from account.models import UserProfile

from feed.models import UserFeedSubscription
import random

def load_sub(user,gender,cnt):
    for i in range(cnt):
        abon = UserProfile.objects.filter(gender=gender).order_by('?')[0]
        print(abon)
        try:
            s = UserFeedSubscription()
            s.user_subscriber = user
            s.user_destination  = abon
            s.save()
        except:
            pass



class Command(BaseCommand):
    'Import feed subscription'
    def handle(self, *args, **options):
        print('Importing feed subscriptions...')
        UserFeedSubscription.objects.all().delete()
        for user in UserProfile.objects.all():
            if user.gender == 'female':
                load_sub(user,'male',3)
            else:
                load_sub(user,'female',3)

            #load_video(user,2)
            
from django.core.management.base import BaseCommand, CommandError
from account.models import UserProfile
from backend.settings import DOMAIN, BASE_DIR
import requests
import sys
import json
from django.core.files import File
from feed.models import UserFeed, UserFeedComment
import random
from feed.tasks import take_pic_from_video
import random

from django_countries.data import COUNTRIES

from usermedia.models import UserMedia


class Command(BaseCommand):
    'Import feed into DB'
    help = 'Import feed into DB'
    def handle(self, *args, **options):
        print('Deleting feeeed...')
        UserFeedComment.objects.all().delete()
            
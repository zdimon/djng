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


def load_comments(f):
    '''
    Adding 4 comments of a random user to the feed object.
    '''
    for i in range(1,4):
        pr = UserProfile.objects.order_by('?').first()
        c = UserFeedComment()
        c.user = pr
        c.feed = f
        c.text = 'Testcomment from %s' % pr
        c.save()



def load_feed(user, cnt):
    '''
    Creating a set of feeds.  

    @param: user - UserProfile object  

    @param: cnt - nubmer of users  
    '''
    for c in range(1,cnt):
        print('Loading... video  %s' % (user))
        i = random.randint(0, len(COUNTRIES) - 1)
        country = COUNTRIES[list(COUNTRIES)[i]]
        i = random.randint(0, len(SITIES) - 1)
        city = SITIES[i]
        f = UserFeed()
        f.is_approved = True
        f.title = 'Test feed of %s %s' % (user,c)
        f.text = 'Test text text text text text feed of %s %s' % (user,c)
        f.user = user
        f.lon = 32.6178
        f.lat = 46.6558
        f.has_video = True
        f.location = '%s %s' % (city, country)
        f.city = city
        f.country = country
        f.save()
        randmain = random.randint(1,3)
        randorient = random.randint(1,3)
        rand_image_count = random.randint(1,4)
        rand_video_count = random.randint(1,4)
        for cnt in range(0,rand_image_count):
            fm = UserMedia()
            fm.feed = f
            fm.user = user
            fm.type_media = 'photo'
            rnd = random.randint(1,10)
            image_path = BASE_DIR+'/test_data/feed/images/%s.jpg' % rnd
            with open(image_path, 'rb') as image:
                fm.image.save('%s.jpeg'% user.id, File(image), save=True)
            if randorient == 2:
                fm.orient = 'land'
            fm.save()
            #if randmain == 2:
            f.last_media = fm
            f.save()


        for cnt in range(0,rand_video_count):
            if randmain != 2:
                fm = UserMedia()
                fm.feed = f
                fm.type_media = 'video'
                fm.user = user
                fm.orient = 'land'
                rnd = random.randint(1,18)
                videopath = BASE_DIR+'/test_data/feed/video/%s.mp4' % rnd
                with open(videopath, 'rb') as image:
                    fm.video.save('%s.jpeg'% user.id, File(image), save=True)
                fm.save()
                take_pic_from_video(fm)
                
                f.last_media = fm
                f.save()

        load_comments(f)


        '''
        rnd = random.randint(1,10)
        filepath = BASE_DIR+'/test_data/feed/images/%s.jpg' % rnd
        videopath = BASE_DIR+'/test_data/feed/video/%s.mp4' % rnd
        with open(filepath, 'rb') as image:
            f.image.save('%s.jpeg'% user.id, File(image), save=True)
        with open(videopath, 'rb') as video:
            f.video.save('%s.mp4'% user.id, File(video), save=True)
        f.has_video = True
        '''
        
    

class Command(BaseCommand):
    'Import feed into DB'
    help = 'Import feed into DB'
    def handle(self, *args, **options):
        print('Importing feeeed...')
        UserFeed.objects.all().delete()
        for user in UserProfile.objects.all():
            #if user.username != 'woman1':
            load_feed(user,2)
            #load_video(user,2)
            
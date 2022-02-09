from django.core.management.base import BaseCommand, CommandError
from account.models import UserProfile
from django.contrib.auth.models import User
from backend.settings import DOMAIN, BASE_DIR
import requests
import sys
import json
from django.core.files import File
from usermedia.models import UserMedia
import random
from usermedia.tasks import take_pic_from_video


def load_video(user, type):
    '''
    Loading video files from /test_data/media/video

    @param: type (role) - 'private/public'

    '''
    print('Loading video...%s' % user)
    p = UserMedia()
    p.user = user
    p.is_approved = True
    p.type_media = 'video'
    p.orient = 'land'
    p.role_media = type
    try:
        filepath = BASE_DIR+'/test_data/media/video/%s.mp4' % (random.randint(1, 20))
        with open(filepath, 'rb') as video:
            p.video.save('%s.mp4' % user.id, File(video), save=True)
        p.save()
        #import pdb; pdb.set_trace()
        take_pic_from_video(p)
    except Exception as ex:
        print(ex)


def load_public_photo(user, gender):
    '''
    Loading images from /test_data/media/photo/ in two orientations
    '''
    print('Loading public photo...%s' % user)
    ror = random.randint(1,3)
    if ror==2:
        orient = 'land'
    else:
        orient = 'port'
    p = UserMedia()
    p.user = user.userprofile
    p.is_approved = True
    p.type_media = 'photo'
    p.orient = orient
    p.role_media = 'public'
    try:
        filepath = BASE_DIR+'/test_data/media/photo/%s%s.jpg' % (random.randint(1, 8), gender)
        with open(filepath, 'rb') as image:
            p.image.save('%s.jpeg' % user.id, File(image), save=True)
        p.save()
        p.setAsMain()
    except Exception as ex:
        print(ex)


def load_buffer_photo(user):
    '''
    Loading images from /test_data/media/photo/ in two orientations
    for buffer zone (adding to chat and not for publication on site) 

    '''
    print('Loading buffer photo...%s' % user)
    p = UserMedia()
    p.user = user.userprofile
    p.is_approved = True
    p.type_media = 'photo'
    p.role_media = 'buffer'
    try:
        filepath = BASE_DIR+'/test_data/media/photo/buffer/%s.jpg' % (random.randint(1, 10))
        with open(filepath, 'rb') as image:
            p.image.save('%s.jpeg' % user.id, File(image), save=True)
        p.save()
    except Exception as ex:
        print(ex)


def load_private_photo(user):
    '''
    Loading private photos.
    '''
    print('Loading private photo...%s' % user)
    p = UserMedia()
    p.user = user.userprofile
    p.is_approved = True
    p.type_media = 'photo'
    p.role_media = 'private'
    try:
        filepath = BASE_DIR+'/test_data/media/photo/private/%s.jpg' % (random.randint(1, 10))
        with open(filepath, 'rb') as image:
            p.image.save('%s.jpeg' % user.id, File(image), save=True)
        p.save()
    except Exception as ex:
        print(ex)


class Command(BaseCommand):
    'Import media content into DB'
    help = 'Import photo into DB'

    def handle(self, *args, **options):
        print('Importing user media...')
        UserMedia.objects.all().delete()
        
        for user in UserProfile.objects.filter(gender='male'):
            load_public_photo(user, 'm')
            load_public_photo(user, 'm')

        for user in UserProfile.objects.filter(gender='female'):
            load_public_photo(user, 'w')
            load_public_photo(user, 'w')
      
        for user in UserProfile.objects.filter(gender='female'):
            load_private_photo(user)
            load_private_photo(user)

        for user in UserProfile.objects.all():
            load_buffer_photo(user)
            load_buffer_photo(user)

        for user in UserProfile.objects.all():
            load_video(user, 'public')
            load_video(user, 'public')
            load_video(user, 'private')
            load_video(user, 'private')
            load_video(user, 'buffer')
            load_video(user, 'buffer')

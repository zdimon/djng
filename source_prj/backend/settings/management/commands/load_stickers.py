from django.core.management.base import BaseCommand, CommandError
from settings.models import AppSettings, Pictures, ReplanishmentPlan
from django_celery_beat.models import IntervalSchedule, PeriodicTasks, PeriodicTask
from backend.settings import BASE_DIR
import glob
from django.core.files import File
import json


def load_stickers():
    Pictures.objects.filter(type_obj='sticker').delete()
    source_dir = BASE_DIR+'/test_data/stickers'
    data_file =  BASE_DIR+'/test_data/stickers.json'
    with open(data_file,'r') as file:
        jdata = json.loads(file.read())
    for s in jdata:
        print(s)
        im = source_dir+'/%s' % s['image']
        p = Pictures()
        p.type_obj ='sticker'
        p.name = s['title']
        with open(im, 'rb') as image:
            p.image.save(s['image'], File(image), save=True)
        p.save()
        print("Import sticker .... %s" % s['image'])
    


class Command(BaseCommand):
    'Import stickers'
    help = 'Import stickers'

    def handle(self, *args, **options):
        load_stickers()
      
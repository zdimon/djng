from django.core.management.base import BaseCommand, CommandError
from settings.models import AppSettings, Pictures, ReplanishmentPlan
from django_celery_beat.models import IntervalSchedule, PeriodicTasks, PeriodicTask
from backend.settings import BASE_DIR
import glob
from django.core.files import File
import json
from .mailtpls import load_mail_tpls
from django.contrib.auth.models import Group



def load_replanisments():
    ReplanishmentPlan.objects.all().delete()
    data = [
        {
            'name': '13 $',
            'dolar': 13,
            'credit': 10
        },
        {
            'name': '13 $',
            'dolar': 13,
            'credit': 40
        },
        {
            'name': '45 $',
            'dolar': 45,
            'credit': 140
        },
        {
            'name': '99 $',
            'dolar': 99,
            'credit': 320
        },
        {
            'name': '149 $',
            'dolar': 149,
            'credit': 500
        },
        {
            'name': '219 $',
            'dolar': 219,
            'credit': 750
        },
        {
            'name': '299 $',
            'dolar': 299,
            'credit': 1070
        },
        {
            'name': '389 $',
            'dolar': 389,
            'credit': 1400
        },
        {
            'name': '459 $',
            'dolar': 459,
            'credit': 1700
        },
        {
            'name': '919 $',
            'dolar': 919,
            'credit': 3400
        },
    ]

    for i in data:
        print('Saving ... %s' % i['name'])
        r = ReplanishmentPlan()
        r.name = i['name']
        r.dollar = i['dolar']
        r.credit = i['credit']
        r.save()

def load_groups():
    Group.objects.all().delete()
    g = Group()
    g.name = 'manager'
    g.save()
    g = Group()
    g.name = 'director'
    g.save()
    g = Group()
    g.name = 'moderator'
    g.save()
    g = Group()
    g.name = 'webmaster'
    g.save()
    g = Group()
    g.name = 'admin'
    g.save()


def load_smiles():
    Pictures.objects.filter(type_obj='smile').delete()
    source_dir = BASE_DIR+'/test_data/smiles'
    data_file =  BASE_DIR+'/test_data/smiles.json'
    with open(data_file,'r') as file:
        jdata = json.loads(file.read())
    for s in jdata:
        print(s)
        im = source_dir+'/%s' % s['image']
        p = Pictures()
        p.alias = s['alias']
        p.type_obj ='smile'
        p.name = s['title']
        try:
            with open(im, 'rb') as image:
                p.image.save(s['image'], File(image), save=True)
            p.save()
        except:
            pass
    '''
    files = []
    for file in glob.glob(source_dir+'/*'):
        files.append(file)
    for i in files:
        arr = i.split('/')
        fname = arr[len(arr)-1]
        print(fname)
        p = Pictures()
        p.alias ='smile'
        with open(i, 'rb') as image:
            p.image.save(fname, File(image), save=True)
        p.save()
        print('Saving...%s' % fname)
    '''


class Command(BaseCommand):
    'Import Aplication settings into DB'
    help = 'Import Aplication Settings into DB'

    def handle(self, *args, **options):
        from datetime import datetime
        from django.utils import timezone
        print('Importing settings...')
        AppSettings.objects.all().delete()
        

        print('Load data in DB')
        AppSettings.objects.create(name='Support Email', value='support@dating-club.com', alias='support')
        AppSettings.objects.create(name='Noreplay Email', value='noreplay@dating-club.com', alias='noreply')
        print('Data loaded!')

        print('Import Intervals')
        IntervalSchedule.objects.all().delete()
        PeriodicTask.objects.all().delete()

        i1 = IntervalSchedule()
        i1.period = 'seconds'
        i1.every = 10
        i1.save()

        i2 = IntervalSchedule()
        i2.period = 'seconds'
        i2.every = 20
        i2.save()

        i3 = IntervalSchedule()
        i3.period = 'minutes'
        i3.every = 1
        i3.save()

        i5 = IntervalSchedule()
        i5.period = 'minutes'
        i5.every = 5
        i5.save()

        p = PeriodicTask()
        p.name = 'clearing offline users'
        p.task = 'online.tasks.remove_offline'
        p.interval = i5
        p.last_update = datetime.now(tz=timezone.utc)
        p.save()

        # p = PeriodicTask()
        # p.name = 'charging for chat messages'
        # p.task = 'payment.tasks.charge_for_chat'
        # p.interval = i1
        # p.last_update = datetime.now(tz=timezone.utc)
        # p.save()

        p = PeriodicTask()
        p.name = 'charging for chat video'
        p.task = 'payment.tasks.charge_for_video'
        p.interval = i2
        p.last_update = datetime.now(tz=timezone.utc)
        p.save()

        p = PeriodicTask()
        p.name = 'update active sockets'
        p.task = 'online.tasks.update_online'
        p.interval = i2
        p.last_update = datetime.now(tz=timezone.utc)
        p.save()

        p = PeriodicTask()
        p.name = 'check pay for video chat'
        p.task = 'chat.tasks.pay_credits_for_video_chat'
        p.interval = i1
        p.last_update = datetime.now(tz=timezone.utc)
        p.save()

        """
            Check empty media in stories
        """
        p = PeriodicTask()
        p.name = 'check empty media in stories'
        p.task = 'feed.tasks.check_empty_stories'
        p.interval = i5
        p.last_update = datetime.now(tz=timezone.utc)
        p.save()

        load_smiles()
        load_replanisments()
        load_mail_tpls()
        load_groups()

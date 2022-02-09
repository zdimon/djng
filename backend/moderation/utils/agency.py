import datetime
import json
from moderation.models import Moderation
from django.utils.safestring import mark_safe
from agency.models import Agency, AgencyFiles
from django.core.files.base import ContentFile
import base64
import random

def add_agency_profile(data):
    print('Adding agency profile')
    m = Moderation()
    m.name = 'Agency registration'
    m.data = json.dumps(data)
    m.type_obj = 'agency'
    m.save()
    return m


def make_agency_html_from_json(obj):
    jdata = json.loads(obj.data)
    out = ''
    for key in jdata:
        if key == 'images':
            imv = ''
            #print(jdata[key])
            for im in jdata[key]:
                imv += '<img width="150" src="%s">' % im
            value = imv
        else:
            value = jdata[key]
        out += '<tr><td><strong>%s:</strong></td><td>%s</td></tr>' % (key, value)
    return mark_safe('<table>%s</table>' % out)


def approve_agency_profile(obj):
    print("Approving")
    data = json.loads(obj.data)
    #print(data)
    
    u = Agency()
    # u.username = data['login']
    u.name =  data['name']
    # u.set_password(data['password'])
    u.is_active = True
    u.is_staff = False
    u.email = data['email']
    u.is_superuser = False
    # u.name_boss = data['name_boss']
    u.address = data['address']
    u.country = data['country']
    u.city = data['city']
    u.phone1 = data['phone1']
    u.phone2 = data['phone2']
    u.skype = data['skype']
    # u.count_woman = data['count_woman']
    # u.working_time = data['working_time']
    u.save()
    
    obj.delete()
    # for im in data['images']:
    #     format, imgstr = im.split(';base64,')
    #     ext = format.split('/')[-1]
    #     data = ContentFile(base64.b64decode(imgstr))
    #     file_name = '%s-%s.%s' % (u.id,random.randint(111,999),ext)
    #     c = AgencyFiles()
    #     c.agency = u
    #     c.image.save(file_name, data, save=True)
    #     c.save()
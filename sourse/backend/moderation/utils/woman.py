import datetime
from math import floor
import json
from moderation.models import Moderation
from django.utils.safestring import mark_safe
from props.models import Props, Value, Value2User
from account.models import UserProfile
from usermedia.models import UserMedia
import random
from django.core.files.base import ContentFile
import base64
from django.utils.dateparse import parse_date

def fillprops(profile, jdata):
    for key in jdata:
        try:
            prop = Props.objects.get(alias=key)
            if isinstance(jdata[key], list):
                out = []
                ops = Value.objects.filter(prop=prop)
                inx = 0
                for v in jdata[key]:
                    if v:
                        v2u = Value2User()
                        v2u.user = profile
                        v2u.value = ops[inx]
                        v2u.prop = prop
                        v2u.save()
                    inx += 1

            else:
                val = Value.objects.get(pk=int(jdata[key]))
                v2u = Value2User()
                v2u.user = profile
                v2u.value = val
                v2u.prop = prop
                v2u.save()
        except Exception as e:
            print(str(e))


def approve_woman_profile(obj):
    print("Approving")
    data = json.loads(obj.data)
    print(data)
    pwd = random.randint(11111, 99999)
    u = UserProfile()
    u.username = data['email']
    u.gender = 'female'
    u.set_password(pwd)
    u.is_active = True
    u.is_staff = False
    u.email = data['email']
    u.is_superuser = False
    u.about_me = data['about_me']
    u.goal = data['goal']
    u.job = data['job']
    u.city = data['city']
    u.lookingfor = data['lookingfor']
    bd = '%s-%s-%s' % (data['birthday'][0:4], data['birthday'][5:7],data['birthday'][8:10])
    print(bd)
    u.birthday = parse_date(bd)
    u.save()
    fillprops(u, data)
    obj.delete()
    for im in data['images']:
        format, imgstr = im.split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr))  
        file_name = '%s-%s.%s' % (u.id,random.randint(111,999),ext)
        c = UserMedia()
        c.user = u
        c.is_approved = True
        c.image.save(file_name, data, save=True)
        c.save() 
        c.setAsMain()


def add_woman_profile(data):
    print('Adding woman profile')
    print(data)
    m = Moderation()
    m.name = 'Woman registration'
    m.data = json.dumps(data)
    m.save()
    return m





def get_par(key, value):
    try:
        prop = Props.objects.get(alias=key)
        if isinstance(value, list):
            out = []
            ops = Value.objects.filter(prop=prop)
            inx = 0
            for v in value:
                if v:
                    out.append(ops[inx].name)
                inx += 1
            return out

        else:
            val = Value.objects.get(pk=value)
            return val
    except:
        return False


def manke_html_from_json(obj):
    jdata = json.loads(obj.data)
    out = ''
    for key in jdata:
        dpar = get_par(key, jdata[key])
        if dpar:
            value = dpar
        else:
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

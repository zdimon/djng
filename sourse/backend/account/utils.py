from django.core.mail import send_mail
from backend.local import EMAIL_HOST_USER
from settings.models import MailTemplates
from django.contrib.gis import geoip2


def send_email(email, template):
    '''
      Sending email message in HTML format.

      Needs to have the settings 
      
        EMAIL_HOST = 'smtp.gmail.com'
        EMAIL_PORT = 587
        EMAIL_HOST_USER = 'email'
        EMAIL_HOST_PASSWORD = 'password'
        EMAIL_USE_TLS = True 


        EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
        
        EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
        EMAIL_FILE_PATH = '/tmp/app-messages' # change this to a proper location

       in the local.py

      @author sj1nd3l@gmail.com
    '''

    send_mail(
        template.title,
        template.content,
        EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    print('Email send!')


def zodiac_sign(obj):
    try:
        day = obj.birthday.day
        month = obj.birthday.month
    except:
        return 'none'
    # day = 1
    # month = 1
    # print(obj.birthday)
    # checks month and date within the valid range 
    # of a specified zodiac 
    if month == 12:
        astro_sign = 'sagittarius' if (day < 22) else 'capricorn'

    elif month == 1:
        astro_sign = 'capricorn' if (day < 20) else 'aquarius'

    elif month == 2:
        astro_sign = 'aquarius' if (day < 19) else 'pisces'

    elif month == 3:
        astro_sign = 'pisces' if (day < 21) else 'aries'

    elif month == 4:
        astro_sign = 'aries' if (day < 20) else 'taurus'

    elif month == 5:
        astro_sign = 'taurus' if (day < 21) else 'gemini'

    elif month == 6:
        astro_sign = 'gemini' if (day < 21) else 'cancer'

    elif month == 7:
        astro_sign = 'cancer' if (day < 23) else 'leo'

    elif month == 8:
        astro_sign = 'leo' if (day < 23) else 'virgo'

    elif month == 9:
        astro_sign = 'virgo' if (day < 23) else 'libra'

    elif month == 10:
        astro_sign = 'libra' if (day < 23) else 'scorpio'

    elif month == 11:
        astro_sign = 'scorpio' if (day < 22) else 'sagittarius'

    return astro_sign


def get_geolocation(ip):
    geoip = geoip2.GeoIP2()
    data = geoip.city(ip)
    response_data = {'country': data['country_name'] or 'unknown', 'city': data['city'] or 'unknown',
                     'long': data['longitude'] or '0', 'lat': data['latitude'] or '0'}
    return response_data


from email_validator import EmailNotValidError, validate_email
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from moderation.utils.woman import add_woman_profile
from moderation.utils.agency import add_agency_profile
import random
from settings.models import MailTemplates
from account.models import UserProfile
from account.utils import send_email
from rest_framework.authtoken.models import Token
from account.user_serializer import ShortUserSerializer
import base64
from django.core.files.base import ContentFile
from usermedia.models import UserMedia
import random
from moderation.utils.photo import moderate_delete, moderate_new


class RegisterWoman(APIView):
    """
    Woman registration.

    Genetating random password.

    Creating record in DB (account.models.UserProfile).

    Creating a new record with the json was taken in the Moderation model.

    Sending email using template (MailTemplates.objects.get(alias=’woman-registration’)).

    moderation.utils.woman.add_woman_profile(json)

    """
    permission_classes = (AllowAny,)
    def post(self, request, format=None):
        print(request.data)
        password = random.randint(1111, 9999)
        email = request.data.get("email")

        # Change email_template
        tpl = MailTemplates.objects.get(alias='woman-registration')
        data = [
            {'name': '{password}', 'value': str(password)},
            {'name': '{username}', 'value': email}
        ]
        # посылаем емайл с паролем
        tpl.parse(data)
        send_email(email, tpl)

        try:
            u = UserProfile()
            u.gender = 'female'
            u.username = email
            u.email = email
            u.is_active = False
            u.set_password(password)
            u.save()
            u.publicname = 'user'+str(u.id)
            u.save()
            token, key = Token.objects.get_or_create(user=u)

            # убрали на регистрацию
            m = add_woman_profile(data)
            return Response({
                'status': 0,
                'message': 'Ok',
                'mod_id': m.id,
                'token': token.key,
                'language': 'en',
                'user': ShortUserSerializer(u).data
            })
        except Exception as ex:
            return Response({
                'status': 9999,
                'message': 'Error. ' + str(ex)
            })


class RegisterAgencyView(APIView):
    """
    Agency registration.

    Creating a new record with the json was taken in the Moderation model.

    moderation.utils.agency.add_agency_profile(json)

    """
    permission_classes = (AllowAny,)
    def post(self, request, format=None):
        m = add_agency_profile(request.data)
        return Response({'status': 0, 'message': 'Ok', 'id': m.id})


class RegisterMan(APIView):
    """
    Man registration.

    Genetating random password.

    Creating record in DB (account.models.UserProfile).

    Sending email using template (MailTemplates.objects.get(alias='man-registration')).

    """
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        password = random.randint(1111, 9999)
        email = request.data.get("email")

        # Change email_template
        tpl = MailTemplates.objects.get(alias='man-registration')
        data = [
            {'name': '{password}', 'value': str(password)},
            {'name': '{username}', 'value': email}
        ]
        print(data)
        tpl.parse(data)
        #
        send_email(email, tpl)
        u = UserProfile()
        u.username = email
        u.email = email
        u.is_active = True
        u.set_password(password)
        u.save()
        u.publicname = 'user'+str(u.id)
        u.save()
        token, key = Token.objects.get_or_create(user=u)

        ###  Saving photo
        photo = request.data.get("photo")
        if photo:
            format, imgstr = photo.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr))
            file_name = '%s-%s.%s' % (u.id, random.randint(111, 999), ext)
            c = UserMedia()
            c.user = u
            c.image.save(file_name, data, save=True)
            c.save()
            moderate_new(c)

        return Response({
            'status': 0, 
            'message': 'Ok', 
            'token': token.key, 
            'language': 'en', 
            'user': ShortUserSerializer(u).data})


class CheckValidEmail(APIView):

    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        try:
            validate_email(email)
            return Response({
                'status': 0,
                'message': 'Valid email'
            })
        except EmailNotValidError as e:
            print(str(e))
        except Exception as e:
            print(str(e))

        return Response({
            'status': 1,
            'message': 'Not valid email'
        })

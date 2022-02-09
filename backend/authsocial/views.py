from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
# Create your views here.
from authsocial.models import SocialAuth
from account.models import UserProfile
from rest_framework.authtoken.models import Token
import requests
from backend.settings import BASE_DIR
from django.core.files import File
import random
from usermedia.models import UserMedia
from online.utils import set_user_offline, set_user_online
from account.user_serializer import user_serializer

class GoogleView(APIView):
    '''

    Auth from google.
    { 
    id: "100864326099254628076", 
    name: "Node JS", 
    email: "dmytromorozzz@gmail.com", 
    photoUrl: "....jpg", 
    firstName: "Node", 
    lastName: "JS", 
    authToken: "....", 
    provider: "GOOGLE" }

    '''
    
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        #print(request.data)
        try:
            a = SocialAuth.objects.get(email=request.data['email'])
            token = Token.objects.get(user=a.user)
            p = a.user
        except Exception as e:
            print(str(e))
            p = UserProfile()
            p.email = request.data['email']
            p.username = request.data['email']
            p.publicname = request.data['firstName']
            p.is_active = True
            p.set_password('auth1auth2')
            p.save()
            a = SocialAuth()
            a.user = p
            a.email = request.data['email']
            a.type='google'
            a.userid = request.data['id']
            a.save()
            token = Token.objects.create(user=p)
            r = requests.get(request.data['photoUrl'], stream=True)
            if r.status_code == 200:
                rint = random.randint(111,9999)
                filename = '%s/tmp/%s.jpg' % (BASE_DIR,rint)
                with open(filename, 'wb') as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
                ph = UserMedia()
                ph.user = p
                ph.is_approved = True
                ph.is_main = True
                with open(filename, 'rb') as image:
                    ph.image.save('%s.jpeg'% p.id, File(image), save=True)
                ph.save()

        data = {
            'token': token.key,  
            'language': p.language,
            'socket_id': request.data['socket_id'],
            'agent':request.META['HTTP_USER_AGENT'],
            'user': p
        }
        set_user_online(data)
        #print(request.data)
        #print(request.data['email'])
        #return Response({'status': 1})
        return Response({
            'token': token.key,
            'agent': request.META['HTTP_USER_AGENT'],
            'user': user_serializer(p)
        })
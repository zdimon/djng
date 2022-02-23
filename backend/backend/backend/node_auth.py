from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from account.models import UserProfile

class NodeAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        print(request)
        user = UserProfile.objects.get(username='man1@gmail.com')
        return (user, None)
        
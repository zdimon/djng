from django.shortcuts import render
from account.models import UserProfile
from account.user_serializer import ShortUserSerializer, user_serializer, UserListItemSerializer
from rest_framework import generics
# Create your views here.

class UserlistAllListView(generics.ListAPIView):
    """
    API endpoint for userlist.
    """
    queryset = UserProfile.objects.all().order_by('-id')
    serializer_class = UserListItemSerializer

    def get_queryset(self):
        try:
            user = self.request.user.userprofile
            if user.gender == 'male':
                return UserProfile.objects.filter(gender='female')
            else:
                return UserProfile.objects.filter(gender='male')
        except:
            return UserProfile.objects.filter(gender='female')

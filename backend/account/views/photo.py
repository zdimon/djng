
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.translation import ugettext_lazy as _
from usermedia.models import UserMedia
from usermedia.serializers import UserMediaPhotoSerializer

from account.user_serializer import ShortUserSerializer

class MyPhotoView(generics.ListAPIView):
    """
    Terurns list of user`s photo.
    """
    queryset = UserMedia.objects.all().order_by('-id')
    serializer_class = UserMediaPhotoSerializer

    def get_queryset(self):
        pr = self.request.user.userprofile
        return UserMedia.objects.filter(user=pr,type_media='photo').order_by('-id')


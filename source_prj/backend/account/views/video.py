
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.translation import ugettext_lazy as _
from usermedia.models import UserMedia
from usermedia.serializers import UserMediaVideoSerializer

from account.user_serializer import ShortUserSerializer


class MyVideoView(generics.ListAPIView):
    """
    Terurns list of user`s video.
    """
    queryset = UserMedia.objects.all()
    serializer_class = UserMediaVideoSerializer

    def get_queryset(self):
        pr = self.request.user.userprofile
        return UserMedia.objects.filter(user=pr,type_media='video')
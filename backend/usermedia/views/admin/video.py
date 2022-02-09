from usermedia.models import UserMedia
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.utils.translation import ugettext_lazy as _
from rest_framework import viewsets
from usermedia.serializers import UserMediaVideoSerializer

class AdminVideoView(viewsets.ModelViewSet):
    serializer_class = UserMediaVideoSerializer
    queryset = UserMedia.objects.all()
    # lookup_field = 'id'
    # def get(self, request, format=None):


from usermedia.models import UserMedia
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.utils.translation import ugettext_lazy as _
from rest_framework import viewsets
from usermedia.serializers import UserMediaVideoSerializer, UserMediaPhotoAdminSerializer
from rest_framework import generics
from rest_framework import pagination
from account.models import UserProfile

class AdminUsermediaListView(generics.ListAPIView):
    serializer_class = UserMediaPhotoAdminSerializer
    queryset = UserMedia.objects.all()
    pagination_class = pagination.LimitOffsetPagination
    # lookup_field = 'id'
    # def get(self, request, format=None):

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = UserProfile.objects.get(pk=user_id)
        # print(user_id)
        return UserMedia.objects.filter(user=user)



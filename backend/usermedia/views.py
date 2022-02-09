from django.shortcuts import render
from .models import UserMedia
from .serializers import UserMediaSerializer
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from moderation.utils.photo import moderate_delete, moderate_new
from rest_framework.response import Response
from django.utils.translation import ugettext_lazy as _

# Create your views here.
class UserMediaPhotoListView(generics.ListAPIView):
    """
    API endpoint for user media photo.
    """
    queryset = UserMedia.objects.all().order_by('-id')
    serializer_class = UserMediaSerializer

    def get_queryset(self):
        role = self.kwargs['role']
        user = self.request.user.userprofile
        if role != 'all':
            return UserMedia.objects.filter(user=user,type_media='photo', role_media=role)
        else:
            return UserMedia.objects.filter(user=user,type_media='photo')

class AddPhotoView(APIView):
    permission_classes = (IsAuthenticated,)
    """
       Saving image from file input
    """
    def post(self, request, format=None):
        profile = request.user.userprofile
        c = UserMedia()
        c.user = request.user.userprofile
        c.type_media = 'photo'
        c.image.save(str(profile.id)+request.data['myfile'].name, request.data['myfile'], save=True)
        c.save()
        moderate_new(c)
        return Response({c.id: UserMediaSerializer(c).data})

    #def perform_create(self, serializer):
        #media = serializer.save()
        #take_pic(video)


class UserMediaVideoViewSet(viewsets.ModelViewSet):
    """
    API endpoint for user media video.
    """
    queryset = UserMedia.objects.all().order_by('-id')
    serializer_class = UserMediaSerializer

    def get_queryset(self):
        user = self.request.user.userprofile
        return UserMedia.objects.filter(user=user,type_media='video')

    def perform_create(self, serializer):
        media = serializer.save()
        #take_pic(video)


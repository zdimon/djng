from django.shortcuts import render
from usermedia.models import UserMedia
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.response import Response
from usermedia.serializers import UserMediaVideoSerializer
from usermedia.tasks import take_pic_from_video
from rest_framework.generics import RetrieveAPIView


from moderation.utils.photo import moderate_delete
from moderation.utils.video import moderate_new_video
from django.utils.translation import ugettext_lazy as _
from rest_framework import status

class UserMediaVideoViewSet(viewsets.ModelViewSet):
    """
    API endpoint for user media video.
    """
    queryset = UserMedia.objects.all().order_by('-id')
    serializer_class = UserMediaVideoSerializer

    def get_queryset(self):
        user = self.request.user.userprofile
        return UserMedia.objects.filter(user=user,type_media='video').order_by('-id')



    def create(self, request, *args, **kwargs):
        if self.check_video(request):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'status': 1, 'message': _('Error on server!')})
        
    def check_video(self,request):
        file_type = self.request.data['video'].content_type.split('/')[0]
        if file_type != 'video':
            return False
        else:
            return True

    def perform_create(self, serializer):
        user = self.request.user.userprofile
        media = serializer.save()
        media.user = user
        media.type_media = 'video'
        #print('Savvving')
        take_pic_from_video(media)
        moderate_new_video(media)
        
        

class UserMediaVideoDetailView(RetrieveAPIView):
    serializer_class = UserMediaVideoSerializer
    queryset = UserMedia.objects.all().order_by('-id')
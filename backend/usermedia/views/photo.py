from rest_framework.parsers import MultiPartParser, JSONParser

from usermedia.models import UserMedia
from usermedia.serializers import UserMediaPhotoSerializer
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from moderation.utils.photo import moderate_delete, moderate_new
from rest_framework.response import Response
import base64
from django.core.files.base import ContentFile
import random
from django.utils.translation import ugettext_lazy as _


# Create your views here.
class UserMediaPhotoListView(generics.ListAPIView):
    """
    API endpoint for user media photo.
    """
    queryset = UserMedia.objects.all().order_by('-id')
    serializer_class = UserMediaPhotoSerializer

    def get_queryset(self):
        role = self.kwargs['role']
        user = self.request.user.userprofile
        if role != 'all':
            return UserMedia.objects.filter(user=user, type_media='photo', role_media=role).order_by('-id')
        else:
            return UserMedia.objects.filter(user=user, type_media='photo').order_by('-id')


class AddPhotoView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserMediaPhotoSerializer
    parser_classes = MultiPartParser, JSONParser
    """
       Saving image from file input
    """

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            data = response.data
            return Response({'status': 0, 'message': _('Photo saved!'), data['id']: data})
        except Exception as e:
            return Response({'status': 1, 'message': str(e)})

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)


class SaveWebcamImage(APIView):
    permission_classes = (IsAuthenticated,)
    """
       Saving image from web camera
    """

    def post(self, request, format=None):
        format, imgstr = request.data.get('imgBase64').split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr))
        file_name = '%s-%s.%s' % (request.user.id, random.randint(111, 999), ext)
        c = UserMedia()
        c.user = request.user.userprofile
        c.image.save(file_name, data, save=True)
        c.save()
        moderate_new(c)
        return Response({c.id: UserMediaPhotoSerializer(c, context={'request': request}).data})


class SetMainView(APIView):
    permission_classes = (IsAuthenticated,)
    """
       Set photo as main
    """

    def post(self, request, format=None):
        try:
            photo = UserMedia.objects.get(pk=request.data['id'])
            photo.setAsMain()
            return Response({'status': 0, 'message': 'set main OK'})
        except Exception as e:
            return Response({'status': 1, 'message': str(e)})


class DeleteView(APIView):
    permission_classes = (IsAuthenticated,)
    """
       Delete photo (mark as deleted)
    """

    def post(self, request, format=None):
        try:
            photo = UserMedia.objects.get(pk=request.data['id'])
            photo.is_deleted = True
            photo.is_moderated = False
            photo.save()
            # moderate_delete(photo)
            return Response({'status': 0, 'message': 'Ok'})
        except Exception as e:
            return Response({'status': 1, 'message': str(e)})


class CropView(APIView):
    permission_classes = (IsAuthenticated,)
    """
       Crop photo 
    """

    def post(self, request, format=None):
        photo = UserMedia.objects.get(pk=request.data['id'])
        # print(request.data['imgpos'])
        # print(request.data['croppos'])

        cropping_land = '%s,%s,%s,%s' % (
        request.data['imgpos_land']['x1'], request.data['imgpos_land']['y1'], request.data['imgpos_land']['x2'],
        request.data['imgpos_land']['y2'])
        croppingpos_land = '%s,%s,%s,%s' % (
        request.data['croppos_land']['x1'], request.data['croppos_land']['y1'], request.data['croppos_land']['x2'],
        request.data['croppos_land']['y2'])

        cropping_port = '%s,%s,%s,%s' % (
        request.data['imgpos_port']['x1'], request.data['imgpos_port']['y1'], request.data['imgpos_port']['x2'],
        request.data['imgpos_port']['y2'])
        croppingpos_port = '%s,%s,%s,%s' % (
        request.data['croppos_port']['x1'], request.data['croppos_port']['y1'], request.data['croppos_port']['x2'],
        request.data['croppos_port']['y2'])

        cropping_square = '%s,%s,%s,%s' % (
        request.data['imgpos_square']['x1'], request.data['imgpos_square']['y1'], request.data['imgpos_square']['x2'],
        request.data['imgpos_square']['y2'])
        croppingpos_square = '%s,%s,%s,%s' % (
        request.data['croppos_square']['x1'], request.data['croppos_square']['y1'],
        request.data['croppos_square']['x2'], request.data['croppos_square']['y2'])

        photo.cropping_land = cropping_land
        photo.croppos_land = croppingpos_land

        photo.cropping_port = cropping_port
        photo.croppos_port = croppingpos_port

        photo.cropping_square = cropping_square
        photo.croppos_square = croppingpos_square

        photo.save()
        photo.update_thumbs()
        return Response({photo.id: UserMediaPhotoSerializer(photo, context={'request': request}).data})

        # return Response({'status': 0})

from django.shortcuts import render
from rest_framework import viewsets
from chat.models import ChatRoom, ChatMessage, ChatContact
from chat.serializers import RoomSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from account.models import UserProfile
from account.serializers import UserSerializer
from chat.tasks import sent_chat_message, send_update_contacts
from chat.rooms_serializer import serialize_rooms, detail_room, serialize_message, serialize_messages_by_room
import time
from chat.utils import check_man_account, send_notification_to_woman
from usermedia.models import UserMedia
from usermedia.serializers import UserMediaVideoSerializer, UserMediaPhotoSerializer
from payment.tasks import send_update_room
from payment.models import Payment


class SendStickerView(APIView):
    """
       Sending sticker
    """
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        print(request.data)
        user = UserProfile.objects.get(id=request.data['user']['id'])
        room = ChatRoom.objects.get(pk=request.data['room']['id'])
        m = ChatMessage()
        m.message = '<img src="%s" />' % request.data['sticker']['image']
        m.room = room
        m.user = user
        m.type = 'sticker'
        m.save()
        try:
            payment = Payment.objects.get(pk=request.data['payment_id'])
            payment.content_object = m
            payment.save()
        except:
            pass
        sent_chat_message(room)
        return Response({'status': 0})

class VideoListView(APIView):
    """
       Get list of users video
    """
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        user = request.user.userprofile
        videos = UserMedia.objects.filter(user=user,type_media='video',is_approved=True).order_by('-id')
        out = []
        for v in videos:
            out.append(UserMediaVideoSerializer(v).data)
        return Response(out)

class PhotoListView(APIView):
    """
       Get list of users photos
    """
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        user = request.user.userprofile
        videos = UserMedia.objects.filter(user=user,type_media='photo',is_approved=True).order_by('-id')
        out = []
        for v in videos:
            out.append(UserMediaPhotoSerializer(v, context={'request': request}).data)
        return Response(out)


class SendVideoView(APIView):
    """
       Sending video
    """
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        user = UserProfile.objects.get(id=request.data['user']['id'])
        room = ChatRoom.objects.get(pk=request.data['room']['id'])
        video = UserMedia.objects.get(pk= request.data['video']['id'])
        m = ChatMessage()
        m.message = '<video controls src="%s" />' % request.data['video']['get_video_url']
        m.room = room
        m.user = user
        if request.data['video']['role_media'] == 'private':
            m.is_private = True
        m.type = 'video'
        m.content_object = video
        m.save()
        try:
            payment = Payment.objects.get(pk=request.data['payment_id'])
            payment.content_object = m
            payment.save()
        except:
            pass
        sent_chat_message(room)
        return Response({'status': 0})

class SendPhotoView(APIView):
    """
       Sending video
    """
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        user = UserProfile.objects.get(id=request.data['user']['id'])
        room = ChatRoom.objects.get(pk=request.data['room']['id'])
        photo = UserMedia.objects.get(pk= request.data['photo']['id'])
        # print(photo)
        m = ChatMessage()
        m.message = '<img src="%s" />' % request.data['photo']['image_big']
        m.room = room
        m.user = user
        if request.data['photo']['role_media'] == 'private':
            m.is_private = True
        m.type = 'photo'
        m.content_object = photo
        m.save()
        try:
            payment = Payment.objects.get(pk=request.data['payment_id'])
            payment.content_object = m
            payment.save()
        except:
            pass
        sent_chat_message(room)
        return Response({'status': 0})
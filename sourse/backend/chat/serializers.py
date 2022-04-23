from django.contrib.auth.models import User
from account.user_serializer import ShortUserSerializer
from .models import ChatRoom, ChatMessage
from rest_framework import serializers
from account.serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    #user = UserSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'message']
        #depth = 2


class RoomSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField('mesages_func')

    def mesages_func(self, obj):
        msg = []
        for m in ChatMessage.objects.filter(room=obj):
            msg.append(MessageSerializer(m).data)
        return msg

    class Meta:
        model = ChatRoom
        fields = ['id', 'messages']


class ChatRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatRoom
        fields = ['id', 'created_at', 'updated_at', 'is_active', 'is_answered',
                  'is_low_account', 'is_video', 'activity']


class ChatMessageSerializer(serializers.ModelSerializer):
    user = ShortUserSerializer()
    room = ChatRoomSerializer()

    class Meta:
        model = ChatMessage
        fields = ['id', 'type', 'room', 'user', 'message', 'created_at',
                  'updated_at', 'is_readed', 'is_private']

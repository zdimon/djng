from rest_framework import viewsets
from chat.models import ChatRoom, ChatMessage, ChatContact
from chat.serializers import RoomSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from account.models import UserProfile
from chat.rooms_serializer import serialize_rooms, detail_room, serialize_message, serialize_messages_by_room
from payment.tasks import send_update_room
from chat.tasks import sent_chat_message
from chat.tasks import send_update_contacts
from chat.utils import send_notify_about_low_account
from payment.utils import make_chat_text_payment

class SendMessageView(APIView):
    """
    Send message to room.

    Check room activity to avoid loose money.

    Mark as readed for current room.

    """
    def post(self, request, format=None):
        user = UserProfile.objects.get(id=request.data['author']['id'])
        room = ChatRoom.objects.get(pk=request.data['room_id'])

        # chek man empty account
        if user.account == 0 and user.gender == 'male':
            print('empty!!!!!')
            send_notify_about_low_account(user)
            return Response({"status": 1, "message": "Low account"})

        m = ChatMessage()
        m.message = request.data['message']
        m.room = room
        m.user = user
        m.save()
        make_chat_text_payment(m)


        # check room activity to avoid loose money
        # room.check_is_active_by_message(m)
        if room.check_first_message():
            send_update_contacts(room.get_abonent(user))

        # mark messages as readed forcurrent rooms
        if room.is_current(room.get_abonent(user)):
            m.mark_as_readed()

        sent_chat_message(room)
        return Response(detail_room(room,request.user.userprofile))



class SendTestMessageView(APIView):
    """
    Send test message to room.

    """
    permission_classes = (AllowAny,)
    def post(self, request, format=None):
        fromuser = UserProfile.objects.get(username=request.data['from'])
        touser = UserProfile.objects.get(username=request.data['to'])
        print(fromuser)
        room = ChatRoom.objects.get(pk=request.data['room'])
        m = ChatMessage()
        m.message = request.data['message']
        m.room = room
        m.user = fromuser
        m.save()
        sent_chat_message(room)
        return Response({'status': 0})

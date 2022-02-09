from rest_framework import viewsets
from chat.models import ChatRoom, ChatMessage, ChatContact
from chat.serializers import RoomSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from account.models import UserProfile
from chat.rooms_serializer import serialize_rooms, detail_room, serialize_message, serialize_messages_by_room
from payment.tasks import send_update_room


class AddRoomView(APIView):
    """

    Adds room or return an existed (ChatRoom.get_room_or_create(owner,abonent)).

    Marks messages as readed (room.mark_as_readed(owner)).

    """
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        owner = UserProfile.objects.get(id=request.data['owner'])
        abonent = UserProfile.objects.get(id=request.data['abonent'])
        room = ChatRoom.get_room_or_create(owner,abonent)
        room.mark_as_readed(owner)
        return Response(detail_room(room,request.user.userprofile))


class RoomViewSet(viewsets.ModelViewSet):
    """
    API endpoint for rooms.
    """
    queryset = ChatRoom.objects.all().order_by('-id')
    serializer_class = RoomSerializer


class SelectRoomView(APIView):
    """
       Select room from the contact list.

       Mark messages as readed.
    """
    def get(self, request, room_id, format=None):
        room = ChatRoom.objects.get(pk=room_id)
        owner = request.user.userprofile
        room.mark_as_readed(owner)
        c = ChatContact.objects.get(owner=owner,room=room)
        c.set_current() 
        return Response(serialize_rooms(request.user.userprofile))


class RoomList(APIView):
    """
    List of rooms.

    Serialize all rooms by the profile of caller.

    serialize_rooms(request.user.userprofile)

    """
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None): 
        return Response(serialize_rooms(request.user.userprofile))


class StopRoomView(APIView):
    """
    Suspend chat room.

    room.close_room_by_stop_button()

    """
    permission_classes = (IsAuthenticated,)
    def get(self, request, room_id, format=None):
        room = ChatRoom.objects.get(pk=room_id)
        room.close_room_by_stop_button()
        send_update_room(room)
        return Response({'status': 0, 'message': 'Ok'})
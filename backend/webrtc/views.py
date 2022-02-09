from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from mediaserver.openvidu_api.api import OpenVidu
from .models import Offer, Ice, Connection, ActiveStream
import json
from chat.models import ChatRoom, ChatContact
from online.models import UserOnline

import time
from account.user_serializer import user_serializer
from account.models import UserProfile
from payment.models import PaymentType, Payment
from payment.utils import process_transaction
from payment.tasks import send_update_room, send_close_room, make_video_transaction
from backend.settings import REDIS_HOST, REDIS_PORT


import redis
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=4)

# Create your views here.


class PaymentView(APIView):
    """
       Make payment for video

    """
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        room = ChatRoom.objects.get(pk=request.data['room_id'])
        room.is_active = True
        room.save()
        user = request.user.userprofile
        make_video_transaction(user,room)
        return Response({'status': 1, 'account': user.account})


class OfferView(APIView):
    """
       Get offer from abonent after click Show cam button.

       
       con.set_offer(json.dumps(request.data['offer']))

       broadcust to all socket connections 

       for uo in UserOnline.objects.filter(user=abonent):
           'action': 'server-action:put_offer'

    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        # time.sleep(2)
        # print(request.data)
        from_user = request.user.userprofile
        # room = ChatRoom.objects.get(pk=request.data['room_id'])
        con = Connection.get_con_by_from_user(from_user)
        print(con)
        print(from_user)
        print(request.data['offer'])
        if con:
            con.set_offer(json.dumps(request.data['offer']))

        # abonent = room.get_abonent(request.user)
        for uo in UserOnline.objects.filter(user_id=request.data['user_id']):
            data = {
                'task': 'put_to_socket',
                'data': {
                    'action': 'server-action:put_offer',
                    'offer': request.data['offer'],
                    # 'room_id': room.id,
                    'user_id': request.data['user_id'],
                    'socket_id': uo.sid
                }
            }
            redis_client.publish('notifications', json.dumps(data))
        return Response({'offer': 'ok'})


class AnswerView(APIView):
    """
       Getting answer from owner

       Input

       request.data['room_id']

       request.data['offer']



    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        # time.sleep(2)
        print(request.data)
        to_user = request.user.userprofile
        room = ChatRoom.objects.get(pk=request.data['room_id'])
        con = Connection.get_con_by_to_user(to_user)

        print(con)
        print(to_user)
        print(request.data['offer'])

        if con:
            con.set_answer(json.dumps(request.data['offer']))

        o = Offer()
        o.user = request.user.userprofile
        o.offer = json.dumps(request.data['offer'])
        o.room = room
        o.save()
        abonent = room.get_abonent(request.user)
        for uo in UserOnline.objects.filter(user=abonent):
            print('sending annnnnswwwwer %s' % uo.sid)
            data = {
                'task': 'put_to_socket',
                'data': {
                    'action': 'server-action:put_answer',
                    'offer': request.data['offer'],
                    'room_id': room.id,
                    'socket_id': uo.sid,
                    'user_id': request.user.userprofile.id
                }
            }
            redis_client.publish('notifications', json.dumps(data))
        # print(abonent)
        return Response({'answer': 'ok'})


class IceView(APIView):
    """
       Get ice
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        # print(request.data)
        room = ChatRoom.objects.get(pk=request.data['room_id'])
        print('ice %s' % request.data['dest'])
        # print(request.data['ice'])

        if request.data['dest'] == 'owner':
            # ice from abonent

            to_user = request.user.userprofile
            con = Connection.get_con_by_to_user(to_user)
            if con:
                con.set_owner_ice(request.data['ice'])

        if request.data['dest'] == 'abonent':
            # ice from owner

            from_user = request.user.userprofile
            con = Connection.get_con_by_from_user(from_user)
            if con:
                con.set_abonent_ice(request.data['ice'])

        abonent = room.get_abonent(request.user)
        for uo in UserOnline.objects.filter(user=abonent):
            data = {
                'task': 'put_to_socket',
                'data': {
                    'action': 'server-action:put_ice',
                    'ice': request.data['ice'],
                    'room_id': room.id,
                    'dest': request.data['dest'],
                    'socket_id': uo.sid,
                    'user_id': request.user.userprofile.id
                }
            }
            redis_client.publish('notifications', json.dumps(data))
        # print(abonent)
        return Response({'ice': 'ok'})


class CameraOnView(APIView):
    """
    Turn camera ON.

    Set 

    profile.is_camera = True

    Publish data to socket to broadcust all users for updating user`s profile.

    data = {
    'task': 'update_user',
    'user': {profile.id: user_serializer(profile)}
    }
    redis_client.publish('notifications', json.dumps(data)) 

    Response({'camera_on': 'ok'})

    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        profile = request.user.userprofile
        profile.is_camera = True
        profile.save()
        try:
            openvidu_api = OpenVidu()
            openvidu_data = openvidu_api.init_session()
            if 'error' not in openvidu_data:
                ActiveStream.objects.create(session_id=openvidu_data['id'], session_created_at=openvidu_data['createdAt'],
                                            session_status=True,
                                            user_profile=profile)

            else:
                message = {'openvidu_error': openvidu_data}
        except Exception as e:
            print(e)
        data = {
            'task': 'update_user',
            'user': {profile.id: user_serializer(profile)},
        }
        redis_client.publish('notifications', json.dumps(data))
        message = {'camera_on': 'ok'}
        return Response(message)


class CameraOffView(APIView):
    """
    Turn camera ON.

    Set 

    profile.is_camera = False

    Publish data to socket to broadcust all users for updating user`s profile.

    data = {
    'task': 'update_user',
    'user': {profile.id: user_serializer(profile)}
    }
    redis_client.publish('notifications', json.dumps(data)) 

    Response({'camera_off': 'ok'})

    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        profile = request.user.userprofile
        profile.is_camera = False
        profile.save()

        #last_session = ActiveStream.objects.filter(user_profile=profile, session_status=True).last()
        
        # if not last_session:
        #     return Response({'error': f'user with {profile.id} has no session yet'})
        # if not last_session.session_status:
        #     return Response({'error': f'user session is closed'})

        try:
            openvidu_api = OpenVidu()
            openvidu_data = openvidu_api.close_session(session_id=last_session.session_id)
            if 'error' not in openvidu_data:
                last_session.session_status = False
                last_session.save()
            else:
                message = {'openvidu_error': openvidu_data}
        except Exception as e:
            print(e)        

        data = {
            'task': 'update_user',
            'user': {profile.id: user_serializer(profile)},
        }
        redis_client.publish('notifications', json.dumps(data))
        message = {'camera_off': 'ok'}

        return Response(message)


class CameraShowView(APIView):
    """
    Show abonent video

    Input

    room_id (request.data['room']['id'])
    abonent_id (request.data['abonent']['id'])

    room.is_video = True

    Create Connection object.
    Connection.create_con_if_not_exist(owner,abonent,room)

    Broatcast to woman`s sockets

    for sock in abonent.get_socket_ids():
        'action': 'server-action:show_cam'
        'user_id': request.data['abonent']['id'],
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        # print(request.data)
        owner = request.user.userprofile
        abonent = UserProfile.objects.get(pk=request.data['abonent']['id'])
        room = ChatRoom.objects.get(pk=request.data['room']['id'])
        contact = ChatContact.objects.get(room=room, owner=owner)
        contact.is_camera = True
        contact.save()
        room.is_video = True
        room.save()

        # Create connection
        # Connection.create_con_if_not_exist(owner,abonent)

        # print(abonent.get_socket_ids())
        for sock in abonent.get_socket_ids():
            print('send show cam to %s' % sock.sid)
            # profile = request.user.userprofile
            # profile.is_camera = False
            # profile.save()
            data = {
                'task': 'put_to_socket',
                'data': {
                    'socket_id': sock.sid,
                    'user_id': owner.id,
                    'action': 'server-action:show_cam'

                }
                # 'user': {profile.id: user_serializer(profile)}
            }
            redis_client.publish('notifications', json.dumps(data))
        return Response({'camera_show': 'ok'})


class CameraHideView(APIView):
    """
      Hide abonent video

            'task': 'put_to_socket',
            'data': {
                'socket_id': sock.sid,
                'user_id': request.data['abonent']['id'],
                'action': 'server-action:hide_cam'
                
            }

    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        # print(request.data)
        room = ChatRoom.objects.get(pk=request.data['room']['id'])
        owner = request.user.userprofile
        abonent = UserProfile.objects.get(pk=request.data['abonent']['id'])
        # Connection.remove_con(owner,abonent)
        room.is_video = False
        room.save()
        contact = ChatContact.objects.get(room=room, owner=owner)
        contact.is_camera = False
        contact.save()
        for sock in abonent.get_socket_ids():
            data = {
                'task': 'put_to_socket',
                'data': {
                    'socket_id': sock.sid,
                    'user_id': request.user.userprofile.id,
                    'action': 'server-action:hide_cam'

                }
            }
            redis_client.publish('notifications', json.dumps(data))

        return Response({'camera_hide': 'ok'})

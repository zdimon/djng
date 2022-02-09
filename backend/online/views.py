from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import UserProfile
from account.serializers import UserSerializer
from rest_framework import generics
from .models import UserOnline
from backend.settings import REDIS_HOST, REDIS_PORT

import json
import redis
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=4)

class UserOnlineViewset(generics.ListAPIView):
    serializer_class = UserSerializer
    model = serializer_class.Meta.model
    paginate_by = 100
    def get_queryset(self):
        queryset = self.model.objects.filter(is_online=True)
        return queryset.order_by('-id')


class UpdateSocketIdView(APIView):
    """
    Updating socket id by token.

    After F5.

    After login.

    Add a new record in UserOnline model.

    Remove an old one by agent and token.

    UserOnline.objects.get(token=token,agent=agent)

    """
    permission_classes = (AllowAny,)
    def post(self, request, format=None):
        print(request.data)
        token = request.data['token']
        socket_id = request.data['socket_id']
        agent = request.META['HTTP_USER_AGENT']
        
        try:
            profile = request.user.userprofile
        except:
            print(request.headers)
            return Response({'status': 1, 'message': 'not authenticated'})
        profile.set_online()
        try:
            print('reqqqqqq')
            uo = UserOnline.objects.get(token=token,agent=agent)
            uo.sid = socket_id
            uo.save()
        except Exception as e:
            print('Can not update socket ID %s %s create a new one' % (socket_id, e))
            uo = UserOnline()
            uo.sid = socket_id
            uo.token = token
            uo.agent = agent
            uo.user = request.user
            uo.save()
        
        #redis_client.publish('notifications',json.dumps({'task': 'user_online'}))
        return Response({'status': 0, 'message': 'OK'})

class UserOnlineListView(APIView):
    """
       List of users online.  

       url: online/list
    """
    permission_classes = (AllowAny,)
    def get(self, request, format=None):
        try:
            user = request.user.userprofile
            if user.gender == 'female':
                g = 'male'
            else:
                g = 'female'
        except:
            g = 'female'
        users_ids = []
        users = {}
        users_list = []
        userlist = UserProfile.objects.filter(gender=g, is_online=True)
        for u in userlist:
            users_ids.append(u.id)

        for u in userlist:
            users_list.append(UserSerializer(u,context={'request': request}).data)
            users[u.id] = UserSerializer(u,context={'request': request}).data   
        return Response({'users_ids': users_ids, 'users': users, 'users_list': users_list})  

class OnlineCountView(APIView):
    """
       Online count
    """
    permission_classes = (AllowAny,)
    def get(self, request, format=None):
        try:
            user = request.user.userprofile
            if user.gender == 'female':
                g = 'male'
            else:
                g = 'female'
        except:
            g = 'female'
        cnt = UserProfile.objects.filter(gender=g,is_online=True).count()
        return Response({'online': cnt})

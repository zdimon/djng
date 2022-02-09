from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

'''
from online.tasks import publish_to_redis
from account.models import UserProfile
from online.utils import set_user_online, set_user_offline

class CeleryTaskView(APIView):
    permission_classes = (AllowAny,)
    """
       Fire celery tasks
    """
    def post(self, request, format=None):
        if request.data['task'] == 'user_offline':
            profile = UserProfile.get_user_by_name(request.data['username'])
            profile.set_offline()
            publish_to_redis.delay(request.data)
            return Response({'status': 0, 'message': 'Ok'})
        if request.data['task'] == 'user_online':
            profile = UserProfile.get_user_by_name(request.data['username'])
            profile.set_online()
            publish_to_redis.delay(request.data)
            return Response({'status': 0, 'message': 'action: user_online - Ok'})        
        if request.data['task'] == 'set_online':
            print('Setting online')
            #set_user_online(request.data)
            return Response({'status': 0, 'message': 'action: set_online - Ok'})    
        if request.data['task'] == 'set_offline':
            print('Setting offline')
            #set_user_offline(request.data)
            return Response({'status': 0, 'message': 'action: set_offline - Ok'})  
        else:
            return Response({'status': 1, 'message': 'Can not find task'})
            

'''
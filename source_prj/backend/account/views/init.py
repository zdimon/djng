
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from backend.settings import LANGUAGES
from account.models import UserProfile
from account.user_serializer import user_serializer, ShortUserSerializer

class InitApp(APIView):
    '''
    
    Initialization request.
    
    {
    'status': 0,
    'message': 'Ok',
    'token': token.key,
    'languges': lng,
    'user': user_serializer(request.user.userprofile),
    'users_online': uo,
    'online_cnt': number
    }

    '''

    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        try:
            token = Token.objects.get(user=request.user)
            if request.user.userprofile.gender=='male':
                uonline = UserProfile.objects.filter(gender='female',is_online=True)
            else:
                uonline = UserProfile.objects.filter(gender='male',is_online=True)
            uo = {}
            for u in uonline:
                uo[u.id] = user_serializer(u)
            lng = []
            for l in LANGUAGES:
                lng.append({'id': l[0], 'name': l[1]})
            return Response({
                'status': 0,
                'message': 'Ok',
                'token': token.key,
                'languges': lng,
                'user': ShortUserSerializer(request.user.userprofile).data,
                'users_online': uo,
                'online': len(uo)
                })
        except:
            return Response({'status': 1, 'message': 'no authorized!'})


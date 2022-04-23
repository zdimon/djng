from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from online.utils import set_user_offline, set_user_online
from account.user_serializer import user_serializer
from django.utils.translation import ugettext_lazy as _
from logsys.mixins.db_log import DatabaseLogMixin
from logsys.mixins.ip_tracking_log import IpTrackingLog
from account.user_serializer import ShortUserSerializer
from rest_framework import serializers

class AuthCustomTokenSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        print(attrs)
        email_or_username = attrs.get('username')
        password = attrs.get('password')

        if email_or_username and password:
            # Check if user sent email
            if validateEmail(email_or_username):
                user_request = get_object_or_404(
                    User,
                    email=email_or_username,
                )

                email_or_username = user_request.username

            user = authenticate(username=email_or_username, password=password)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise exceptions.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Must include "email or username" and "password"')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs


class LogoutView(DatabaseLogMixin, APIView):
    '''
    Logout.
    '''
    permission_classes = (AllowAny,)
    log_type = 'logout'

    def get(self, request):
        if request.user.is_authenticated:
            token, created = Token.objects.get_or_create(user=request.user)
            set_user_offline({'token': token, 'user': request.user.userprofile})
        else:
            print("User is not authenticated!")
        return Response({'status': 0, 'message': 'Ok'})

# , ObtainAuthToken
class CustomAuthToken(IpTrackingLog, ObtainAuthToken):
    '''
        Login endpoint.

        POST (body json)

        @param: username:str

        @param: password:str

        Checking out login and password and setting user online.
    '''
    log_type = 'login'

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        # serializer = AuthCustomTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        profile = user.userprofile
        # is blocked
        if profile.is_blocked:
            return Response({
                'status': 1, 
                'user': ShortUserSerializer(profile).data,
                'message': _('Your account is blocked!')   
            })        
        profile.set_online()
        token, created = Token.objects.get_or_create(user=user)
        groups = []
        for g in profile.groups.all():
            groups.append(g.name)
        data = {
            'token': token.key,
            # 'socket_id': request.data['socket_id'],
            'language': profile.language,
            'agent': request.META['HTTP_USER_AGENT'],
            'user': profile
        }
        set_user_online(data)

        return Response({
            'token': token.key,
            'agent': request.META['HTTP_USER_AGENT'],
            # 'user': ShortUserSerializer(profile).data,
            'user': ShortUserSerializer(profile).data,
            # 'sid':  request.data['socket_id'],
            'groups': groups
        })

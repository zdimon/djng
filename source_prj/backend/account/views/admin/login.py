'''
    Login endpoint for admin interface.
'''
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

class AdminLoginView(ObtainAuthToken):
    '''
        Login endpoint for admin interface.

        POST (body json)

        @param: username:str

        @param: password:str

        Checking out login and password and setting user online.
    '''
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})

        if not serializer.is_valid(raise_exception=False):
            return Response({
                'status': 1,
                'message': _('Login or password is incorect!')
            })             
        user = serializer.validated_data['user']
        token, create = Token.objects.get_or_create(user=user) 
        groups = []
        for g in user.groups.all():
            groups.append(g.name)
        
        return Response({
            'groups': groups,
            'accessToken': token.key
        })

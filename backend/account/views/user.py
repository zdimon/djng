from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import generics
from account.serializers.user import UserSerializer
from account.filters.user import UserFilter
from django_filters.rest_framework import DjangoFilterBackend

class AdminUserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filterset_fields = ['username', 'email']
    filter_class = UserFilter
    filter_backends = DjangoFilterBackend,

class AdminUserView(APIView):
    permission_classes = {IsAuthenticated}

    def get(self, request, *args, **kwargs):
        token, created = Token.objects.get_or_create(user=request.user)
        groups = []
        for g in request.user.groups.all():
            groups.append(g.name)

        data = {
            'id': request.user.id,
            'username': request.user.username,
            'password': 'demo',
            'email': 'admin@demo.com',
            'accessToken': token.key,
            'refreshToken': 'access-token-f8c137a2c98743f48b643e71161d90aa',
            'roles': groups,
            'pic': '',
            'fullname': 'Sean',
            'occupation': 'CEO',
            'companyName': 'Keenthemes',
            'phone': '456669067890',
            'address': {
                'addressLine': 'L-12-20 Vertex, Cybersquare',
                'city': 'San Francisco',
                'state': 'California',
                'postCode': '45000'
            },
            'socialNetworks': {
                'linkedIn': 'https://linkedin.com/admin',
                'facebook': 'https://facebook.com/admin',
                'twitter': 'https://twitter.com/admin',
                'instagram': 'https://instagram.com/admin'
            }
        }

        return Response(data)

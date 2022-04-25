from django.utils.translation import ugettext_lazy as _
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from account.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from account.views.admin.filters import UserFilter
from rest_framework import generics


class AdminUserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # filter_backends = DjangoFilterBackend,
    filterset_fields = ['username', 'email', 'is_superuser', 'is_staff', 'is_active']
    filter_class = UserFilter


class AdminUserView(APIView):
    permission_classes = {IsAuthenticated}

    def get(self, request, *args, **kwargs):
        try:
            pr = self.request.user.agencyprofile
            print(pr)
        except:
            print('No agency')

        try:
            pr = self.request.user.webmaster
            print(pr)
        except:
            print('No agency')

        try:
            pr = self.request.user.userprofile
            print(pr)
        except:
            print('No agency')

        try:
            pr = self.request.user.adminprofile
            print(pr)
        except:
            print('No agency')

        token, created = Token.objects.get_or_create(user=request.user)

        groups = []
        for g in pr.groups.all():
            groups.append(g.name)

        data = {
            'id': pr.id,
            'username': pr.username,
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

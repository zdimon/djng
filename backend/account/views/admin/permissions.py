from django.utils.translation import ugettext_lazy as _
from rest_framework.response import Response
from rest_framework.views import APIView

class AdminPermissionsView(APIView):

    def get(self, request, *args, **kwargs):
        data = [
            {
                'id': 1,
                'name': 'accessToECommerceModule',
                'level': 1,
                'title': 'eCommerce module'
            },
            {
                'id': 2,
                'name': 'accessToAuthModule',
                'level': 1,
                'title': 'Users Management module'
            }
        ]
        return Response(data)
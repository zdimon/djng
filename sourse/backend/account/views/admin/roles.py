from django.utils.translation import ugettext_lazy as _
from rest_framework.response import Response
from rest_framework.views import APIView

class AdminRolesView(APIView):

    def get(self, request, *args, **kwargs):
        data = [
            {
                'id': 1,
                'title': 'Administrator',
                'isCoreRole': True,
                'permissions': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            }
        ]
        return Response(data)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from account.utils import get_geolocation


class SetLanguageView(APIView):
    permission_classes = (IsAuthenticated,)
    """
       Seting language
    """

    def get(self, request, language, format=None):
        profile = request.user.userprofile
        profile.language = language
        profile.save()
        return Response({'status': 0, 'message': 'ok'})


class GeoLocationView(APIView):
    def get(self, request):
        try:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            ip_address = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
            print(ip_address)
            response_data = get_geolocation(ip_address)
        except Exception as e:
            response_data = {'status': 1, 'message': 'Error', 'detail': e.__str__()}
        return Response(response_data)

from rest_framework.views import APIView
from account.user_serializer import ShortUserSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from chat.models import ChatContact


class FavoriteUsersView(APIView):

    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        profile = request.user.userprofile
        out = []
        for u in ChatContact.objects.filter(owner=profile):
            out.append(u.abonent.id)
        return Response(out)

    

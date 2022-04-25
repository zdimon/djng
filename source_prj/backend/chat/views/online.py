from rest_framework.views import APIView
from account.user_serializer import ShortUserSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from account.models import UserProfile


class OnlineUsersView(APIView):

    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        profile = request.user.userprofile

        out = []
        for u in UserProfile.objects.filter(is_online=True,gender=profile.getOppositeGender()).exclude(id=profile.id):
            out.append(u.id)
        return Response(out)

    

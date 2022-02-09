from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from blocklist.models import BlockList


class AddToBlocklistView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        profile_id = request.data.get("profile_id")
        BlockList.objects.get_or_create(profile_id=profile_id, block_by_user=request.user)
        return Response(
            {'status': 0, 'message': f'user profile with id {profile_id} was added to {request.user} blocklist'})


class RemoveFromBlocklistView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        profile_id = request.data.get("profile_id")
        BlockList.objects.filter(profile_id=profile_id, block_by_user=request.user).delete()
        return Response(
            {'status': 0, 'message': f'user profile with id {profile_id} was removed from {request.user} blocklist'})

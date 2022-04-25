
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
import os
import subprocess
from .tasks import build_front, build_dev

class BuildView(APIView):
    """
       Build angular app on current branch
    """
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        build_front.delay()
        return Response({'status': 0, 'message': 'Ok'})


    def post(self, request, format=None):
        build_front.delay()
        return Response({'status': 0, 'message': 'Ok'})

class BuildDevView(APIView):
    """
       Build angular app on current branch
    """
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        build_dev.delay()
        return Response({'status': 0, 'message': 'Ok'})


    def post(self, request, format=None):
        build_dev.delay()
        return Response({'status': 0, 'message': 'Ok'})
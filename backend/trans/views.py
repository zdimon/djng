from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
# Create your views here.
from .models import TRANS_MAP
from django.utils import translation

class TransView(APIView):
    """
      Get translation messages
    """
    permission_classes = (AllowAny,)
    def get(self, request, lang):
        translation.activate(lang)
        return Response(TRANS_MAP)
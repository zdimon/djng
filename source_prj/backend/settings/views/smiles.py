from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from payment.models import Payment
from settings.models import ReplanishmentPlan, Pictures
from rest_framework.response import Response
from account.models import ReplenishmentLog
from backend.local import DOMAIN
from settings.serializers import SmileSerializer

class SmilesListView(generics.ListAPIView):
    """
    List of smiles
    """
    queryset = Pictures.objects.filter(type_obj='smile')
    serializer_class = SmileSerializer




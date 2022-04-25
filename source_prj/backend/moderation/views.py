from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from moderation.models import Moderation
from moderation.serializers import ModerationSerializer
from moderation.filters import ModerationFilter

class ModerationViewSet(viewsets.ModelViewSet):
    serializer_class = ModerationSerializer
    queryset = Moderation.objects.all()
    filterset_fields = ['type_obj']
    filter_class = ModerationFilter
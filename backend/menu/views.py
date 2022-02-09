from django.shortcuts import render

# Create your views here.

from rest_framework import generics

from menu.models import Menu
from menu.serializers import MenuSerializer



class MenuView(generics.ListAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

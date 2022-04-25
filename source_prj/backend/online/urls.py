from django.urls import path, include
from .views import *
from rest_framework import routers
from .views import UserOnlineListView, UpdateSocketIdView, OnlineCountView



urlpatterns = [

    path('list', UserOnlineListView.as_view(), name="user-online-list"),
    path('update/socket/id', UpdateSocketIdView.as_view(), name="update-socket-id"),
    path('count', OnlineCountView.as_view(), name="user-online-count"),
]

from django.urls import path, include
from .views import *
from rest_framework import routers
from .views import GalleryListView, GalleryDetailView



urlpatterns = [
    path('list/online/<str:online>', GalleryListView.as_view(), name="gallery-list"),
    path('list/online/<str:online>/agefrom/<str:age_from>/ageto/<str:age_to>', GalleryListView.as_view(), name="gallery-list"),
    path('detail/<str:id>', GalleryDetailView.as_view(), name="gallery-detail"),
]

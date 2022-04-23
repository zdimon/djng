from django.urls import path, include
from .views import PostListView

urlpatterns = [

    path('list', PostListView.as_view(), name='post-list'),
    

]
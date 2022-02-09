from django.urls import path, include
from .views import SearchTagView, SearchTagPersonViewSet, SearchTagFeedViewSet




urlpatterns = [
    # path('tag/<str:keyw>/<int:limit>/<int:offset>', SearchTagView.as_view()),


    path('tags-person', SearchTagPersonViewSet.as_view({'get': 'list'})),
    path('tags-feed', SearchTagFeedViewSet.as_view({'get': 'list'}))


]

from django.urls import path
from .views import AddToBlocklistView, RemoveFromBlocklistView


urlpatterns = [
    path('add/', AddToBlocklistView.as_view(), name='add-to-blocklist'),
    path('remove/', RemoveFromBlocklistView.as_view(), name='remove-from-blocklist'),
]


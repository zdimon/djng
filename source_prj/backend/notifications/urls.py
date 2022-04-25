from django.urls import path, include

from notifications.views import NotificationsView

urlpatterns = [
    path('get/<str:type>', NotificationsView.as_view())
]

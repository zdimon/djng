from django.urls import path

from .views import SubscriptionViewSet
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'services', SubscriptionLimitsViewSet, basename='user')
urlpatterns = [
    path('services/limits', SubscriptionViewSet.as_view({'get': 'list'})),
    # path('services/use', SubscriptionViewSet.as_view({'post': 'partial_update'}))
]

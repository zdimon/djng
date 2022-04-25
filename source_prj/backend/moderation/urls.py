from django.urls import path
from rest_framework import routers
# from .admin import moderator_site
from moderation.views import ModerationViewSet
router = routers.SimpleRouter()

urlpatterns = [
    
    
]

router.register(r'moderation/admin', ModerationViewSet)

urlpatterns += router.urls
from django.urls import path, re_path
from .views import OpenViduView


urlpatterns = [
    path('sessions/init', OpenViduView.as_view({'post': 'init_session'}), name="init-session"),
    # optional session_id
    re_path(r'^sessions/get/(?:(?P<session_id>\d+)/)?$', OpenViduView.as_view({'get': 'get_active_sessions'}), name="get-sessions"),
    # path('sessions/get/<session_id>', OpenViduView.as_view({'get': 'get_active_sessions'}), name="get-sessions"),
    path('sessions/close/<int:session_id>', OpenViduView.as_view({'delete': 'close_session'}), name="close-session"),
    path('token/get', OpenViduView.as_view({'post': 'get_token'}), name="get-sessions"),
]


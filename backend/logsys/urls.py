from django.urls import path
from logsys.views import LogViewSet

urlpatterns = [
    path('list/', LogViewSet.as_view({'get': 'list'}), name="logs-get"),
    path('delete/', LogViewSet.as_view({'post': 'destroy'}), name="logs-delete"),
    path('delete/bulk', LogViewSet.as_view({'post': 'bulkDelete'}), name="logs-bulk-delete"),
    path('create/', LogViewSet.as_view({'post': 'create'}), name="logs-create"),
    path('update/', LogViewSet.as_view({'patch': 'update'}), name="logs-update"),
]
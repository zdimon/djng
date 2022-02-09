from django.urls import path
from account.views.admin.user import AdminUserListView

urlpatterns = [

    path('list/', AdminUserListView.as_view(), name="admin-user-list"),

]

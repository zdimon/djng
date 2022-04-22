from django.urls import path, include


from account.views.login import AdminLoginView
from account.views.user import AdminUserView, AdminUserListView
from account.views.menu import MenuView

urlpatterns = [
    path('adminLogin', AdminLoginView.as_view(), name="account-admin-login"),
    path('adminUser', AdminUserView.as_view(), name="account-admin-user"),
    path('menu/get/', MenuView.as_view(), name="menu-get"),
    path('user/list', AdminUserListView.as_view(), name="admin-user-list"),
]

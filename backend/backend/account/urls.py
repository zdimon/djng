from django.urls import path, include


from account.views.login import AdminLoginView


urlpatterns = [
    path('adminLogin', AdminLoginView.as_view(), name="account-admin-login")
]

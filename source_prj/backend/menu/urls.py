from django.urls import path
from menu.views import MenuView

urlpatterns = [

    path('get/', MenuView.as_view(), name="menu-get"),

]

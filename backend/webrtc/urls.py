from django.urls import path, include
from .views import *
from rest_framework import routers
from .views import OfferView, AnswerView, PaymentView, CameraOnView, CameraOffView, CameraShowView, CameraHideView



urlpatterns = [

    path('offer', OfferView.as_view(), name="webrtc-offer"),
    path('answer', AnswerView.as_view(), name="webrtc-answer"),
    path('ice', IceView.as_view(), name="webrtc-ice"),
    path('cameraOn', CameraOnView.as_view(), name="webrtc-camera-on"),
    path('cameraOff', CameraOffView.as_view(), name="webrtc-camera-off"),
    path('cameraShow', CameraShowView.as_view(), name="webrtc-camera-show"),
    path('cameraHide', CameraHideView.as_view(), name="webrtc-camera-hide"),

    path('payment', PaymentView.as_view(), name="webrtc-camera-payment"),

    
]

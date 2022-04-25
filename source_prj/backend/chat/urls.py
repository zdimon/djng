from django.urls import path, include
from rest_framework import routers

from chat.views.room import AddRoomView, StopRoomView, RoomList, SelectRoomView
from chat.views.message import SendMessageView, SendTestMessageView
from chat.views.media import SendStickerView, VideoListView, PhotoListView, SendVideoView, SendPhotoView
from chat.views.online import OnlineUsersView

from chat.views.favorites import FavoriteUsersView

urlpatterns = [

    # room.py

    path('add', AddRoomView.as_view(), name="room-add"),
    path('list', RoomList.as_view(), name="room-list"),
    path('select/<int:room_id>', SelectRoomView.as_view(), name="room-select"),
    path('stop/<int:room_id>', StopRoomView.as_view(), name="room-resume"),

    #message.py

    path('message', SendMessageView.as_view(), name="room-send-message"),
    path('messagetest', SendTestMessageView.as_view(), name="room-send-test-message"),
    
    # media.py

    path('send/sticker', SendStickerView.as_view(), name="room-resume"),
    path('get/video/list', VideoListView.as_view(), name="room-get-video-list"),
    path('get/photo/list', PhotoListView.as_view(), name="room-get-photo-list"),
    path('send/video', SendVideoView.as_view(), name="room-send-video"),
    path('send/photo', SendPhotoView.as_view(), name="room-send-photo"),

    path('online/list', OnlineUsersView.as_view(), name="chat-online-users"),
    path('favorite/list', FavoriteUsersView.as_view(), name="chat-favorites-users"),


]

from django.urls import path, include
from rest_framework import routers
from usermedia.views.photo import UserMediaPhotoListView, AddPhotoView, SetMainView, DeleteView, CropView, SaveWebcamImage
from usermedia.views.video import UserMediaVideoViewSet, UserMediaVideoDetailView
from usermedia.views.media import ChangeRoleMediaView
from usermedia.views.admin.video import AdminVideoView
from usermedia.views.media import GetPrivateMediaView, PayPrivateMediaView
from usermedia.views.admin.media import AdminUsermediaListView
from rest_framework import routers
router = routers.SimpleRouter()

urlpatterns = [

    path('photo/list/<str:role>', UserMediaPhotoListView.as_view(), name='media-photo-list'),
    path('save/webcam/image', SaveWebcamImage.as_view(), name='media-photo-save-webcam'),
    path('add/image', AddPhotoView.as_view()),
    path('setmain', SetMainView.as_view(), name='media-photo-setmain'),
    #path('list', PhotoListView.as_view(), name='photo-list'),
    path('delete', DeleteView.as_view(), name='media-photo-delete'),
    path('crop', CropView.as_view(), name='media-photo-crop'),
    path('video/detail/<int:pk>', UserMediaVideoDetailView.as_view(), name='media-video-detail'),
    path('video', UserMediaVideoViewSet.as_view({
    'get': 'list',
    'post': 'create'
    }), name='media-video-list'),

    path('change/role', ChangeRoleMediaView.as_view(),name='media-change-role'),
    path('get/private', GetPrivateMediaView.as_view(),name='media-get-private-media'),
    path('pay/private', PayPrivateMediaView.as_view(),name='media-pay-private-media'),

    path('api/tab/list/<int:user_id>', AdminUsermediaListView.as_view(),name='media-admin-list'),


]

router.register(r'admin/video', AdminVideoView)
urlpatterns += router.urls


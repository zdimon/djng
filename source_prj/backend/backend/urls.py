from django.contrib import admin
from django.urls import path, include
from backend.settings import ADMIN_CMS_PANEL_URL
from account.views.init import InitApp
from agency.admin import AgencyAdminSite
from online.views import UserOnline 
from page.views import index
from shop.views import ProductViewSet
from .settings import MEDIA_ROOT, MEDIA_URL, DEBUG

from rest_framework import routers

from .rootrouter import RootRouter
from rest_framework.authtoken import views
#from chat.views import RoomViewSet

from feed.views import FeedViewSet, UserFeedCommentView, UserFeedCommentDetail

from account.views.profile import UserProfileViewSet, UserViewSet, CheckEmail



from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Dating club API')

router = RootRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', UserProfileViewSet)
#router.register(r'room', RoomViewSet)
#router.register(r'payment', PaymentViewSet)
router.register(r'feed', FeedViewSet)
router.register(r'product', ProductViewSet)
#router.register(r'search', SearchTagViewSet.as_view({'get': 'list'}), basename='searchtagpersons')

admin.autodiscover()

 
from account.views.auth import CustomAuthToken, LogoutView
#from backend.celery_view import CeleryTaskView

from backend.build_view import BuildView, BuildDevView



urlpatterns = [
    path('build', BuildView.as_view()),
    path('builddev', BuildDevView.as_view()),
    path('swagger', schema_view),
    # path('', include(router.urls)),
    # path('', admin.site.urls),
    path('search/', include('search.urls')),
    path('userlist/', include('userlist.urls')),
    path('post/', include('post.urls')), 
    path('rosetta/', include('rosetta.urls')),
    path('i18n/', include('trans.urls')),
    path('room/', include('chat.urls')),
    path('auth/', include('rest_framework_social_oauth2.urls')),
    path('feed/custom/', include('feed.urls')),
    path('authsocial/', include('authsocial.urls')),
    path('notifications/', include('notifications.urls')),

    path('settings/', include('settings.urls')),
    path('payment/', include('payment.urls')),
    path('online/', include('online.urls')),
    path('usermedia/', include('usermedia.urls')),
    path('webrtc/', include('webrtc.urls')),
    path('account/', include('account.urls')),
    path('props/', include('props.urls')),
    path('gallery/', include('gallery.urls')),
    path('admin/', admin.site.urls),
    # path('admin/', include('account.urls_dashboard')),
    path('agency/', include('agency.urls')),
    path('admin/ajax/', include('grappelli_extras.ajax_urls')),
    path('admin/extras/', include('grappelli_extras.extras_urls')),
    #path(r'api-token-auth/', obtain_jwt_token),
    #path(r'api-token-refresh/', refresh_jwt_token),
    path(r'api-token-auth/', CustomAuthToken.as_view()),
    path(r'init/', InitApp.as_view()),
    path(r'logout/', LogoutView.as_view(),name='user-logout'),
    path(r'check/email', CheckEmail.as_view()),
    #path(r'celery/task', CeleryTaskView.as_view(),name='celery-task'),
    path('grappelli/', include('grappelli.urls')),
    # path('payment/', include('payment.urls')),
    path(r'commentfeed/', UserFeedCommentView.as_view()),
    path(r'commentfeed/<int:pk>', UserFeedCommentDetail.as_view()),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('profile-block/', include('blocklist.urls')),
    path('subscription/', include('subscription.urls')),
    path('static-pages/', include('page.urls')),

    ##### Admin rest routes

    path('logs/', include('logsys.urls')),
    path('profile-block/', include('blocklist.urls')),
    path('likes/', include('likes.urls')),
    path('menu/', include('menu.urls')),
    path('user/', include('account.admin_urls')),
    # path('', include('webmaster.urls')),
    # path('', include('moderation.urls')),
    path('mediaserver/', include('mediaserver.urls')),
    path('', include('adminpanel.urls')),
    path(ADMIN_CMS_PANEL_URL, include('adminpanel.urls'))

]
if DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include
from .settings import MEDIA_ROOT, MEDIA_URL, DEBUG


urlpatterns = [
    path('admin/', admin.site.urls),
   path('account/', include('account.urls')),
]
if DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

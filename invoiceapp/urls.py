from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from django.urls import re_path as url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('invoice.urls')),
    ]
if not settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
        url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    ]
else:
    pass
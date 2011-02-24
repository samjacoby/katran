from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
#    url(r'^(P?<type>books)/(P?<entry_id>\d+)/$', include('entries.urls')),
#    url(r'^(P?<type>typography)/(P?<entry_id>\d+)/$', include('entries.urls')),
#    url(r'^(P?<type>news)/(P?<entry_id>\d+)/$', include('entries.urls')),
#    url(r'^stamps/', include('stamps.urls')),
    url(r'^', include('cms.urls')),
)

if settings.DEBUG:
    urlpatterns = patterns('',
        (r'^' + settings.MEDIA_URL.lstrip('/'), include('appmedia.urls')),
    ) + urlpatterns

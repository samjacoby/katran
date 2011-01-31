from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from django.views.generic import ListView
from entries.models import News

admin.autodiscover()

urlpatterns = patterns('',
    (r'^', ListView.as_view(
           queryset=News.manager.get_all_news(),
           context_object_name = 'list',
           template_name = 'entries/index.html',
    )),
)

if settings.DEBUG:
    urlpatterns = patterns('',
        (r'^' + settings.MEDIA_URL.lstrip('/'), include('appmedia.urls')),
    ) + urlpatterns

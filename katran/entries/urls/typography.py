from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from django.views.generic import ListView, DetailView
from entries.models import Typography

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 
        ListView.as_view(
            queryset=Typography.manager.get_all_typography(),
            context_object_name = 'list',
            template_name = 'entries/index.html')),
    url(r'^(?P<order>\d+)/$', 'entries.views.typography_detail', { 'entry_type': '0' }, name='typography_detail'),

)


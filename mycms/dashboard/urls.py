from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('dashboard.views',
    # Request index.html when nothing else is listed
    url(r'^$', 'index', name="dashboard_index"),
    url(r'^action/$', 'action')
)

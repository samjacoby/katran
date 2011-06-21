from django.conf.urls.defaults import *

urlpatterns = patterns('stamps.views',
        (r'^$', 'index'),
        url(r'^(?P<designer>\w+)/$', 'detail', name='designer'),
        (r'^(?P<designer>\w+)/(?P<family>\d+)/$', 'detail'),
        (r'^(?P<designer>\w+)/(?P<family>\d+)/(?P<stamp>\d+)/$', 'detail'),
        url(r'^(?P<designer>\w+)/(?P<family>\d+)/(?P<stamp>\d+)/(?P<url_override>\w+)/$', 'detail', name='stamp-detail-url'),
        )

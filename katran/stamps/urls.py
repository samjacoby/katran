from django.conf.urls.defaults import *

urlpatterns = patterns('stamps.views',
        (r'^$', 'index'),
        url(r'^(?P<designer>\w+)/$', 'detail', name='designer'),
        (r'^(?P<designer>\w+)/(?P<family>\d+)/$', 'detail'),
        (r'^(?P<designer>\w+)/(?P<family>\d+)/(?P<stamp>\d+)/$', 'detail'),
        )

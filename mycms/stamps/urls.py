from django.conf.urls.defaults import *

urlpatterns = patterns('stamps.views',
        (r'^$', 'index'),
        (r'^(?P<designer>\w+)/$', 'detail'),
        (r'^(?P<designer>\w+)/(?P<family>\d+)/$', 'detail'),
        (r'^(?P<designer>\w+)/(?P<family>\d+)/(?P<stamp>\d+)/$', 'detail'),
        )

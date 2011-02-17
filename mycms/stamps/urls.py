from django.conf.urls.defaults import *
urlpatterns = patterns('stamps.views',
        (r'^$', 'index'),
        (r'^(?P<designer_name>\w+)/$', 'stamp'),
        (r'^(?P<designer_name>\w+)/(?P<stamp_family_id>\d+)/$', 'stamp'),
        (r'^(?P<designer_name>\w+)/(?P<stamp_family_id>\d+)/(?P<stamp_id>\d+)/$',
            'stamp'),
        )

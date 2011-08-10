from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from django.views.generic import ListView, DetailView
from entries.models import Book

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 
        ListView.as_view(
            queryset=Book.manager.get_all_books(),
            context_object_name = 'list',
            template_name = 'entries/index.html')),
    url(r'^books/(?P<order>\d+)/$', 'entries.views.book_detail', { 'entry_type': '1' }, name='book_detail'),

)


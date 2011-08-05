from django.contrib import admin
from django.db import models
from django.forms import ModelForm
from cms.admin.placeholderadmin import PlaceholderAdmin
from entries.models import Book, Typography

class BaseClass( PlaceholderAdmin ):
    
    list_display = ('title', 'subtitle', 'order')
    list_editable = ['order']
    exclude = ('order', 'entry_type')

    def __unicode__(self):
        self.title

    def queryset(self, request):
        qs = super( PlaceholderAdmin, self ).queryset(request)
        qs = qs.filter( entry_type=self.entry_type )
        return qs

class TypographyAdmin( BaseClass ):

    entry_type = 0 # Typography
    
class BookAdmin( BaseClass ):

    entry_type = 1 # Book


admin.site.register( Book, BookAdmin ) 
admin.site.register( Typography, TypographyAdmin )

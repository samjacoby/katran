from django.contrib import admin
from django.db import models
from django.forms import ModelForm
from cms.admin.placeholderadmin import PlaceholderAdmin
from entries.models import Book, Typography, News


#class EntryForm( ModelForm ):
#    model = EntryRelationship
#    class = Media:
#        js = ( 'js/jquery-1.4.4.min.js',
#               'js/jquery-ui-1.8.9.custom.min.js',
#               'js/menu-sort.js', 
#               )


#class EntryRelationshipInline( admin.StackedInline ):
#    model = EntryRelationship
#    fk_name = 'entry'
#    extra = 0
#    ordering = ('order',)


#from cms.plugins.text.widgets.wymeditor_widget import WYMEditor
class BaseClass( PlaceholderAdmin ):
    
    list_display = ('title', 'subtitle', 'order')
    list_editable = ['order']
    exclude = ('order', 'entry_type')

#    inlines = [ EntryRelationshipInline ]                                 

    def __unicode__(self):
        self.title

    def queryset(self, request):
        qs = super( PlaceholderAdmin, self ).queryset(request)
        qs = qs.filter( entry_type=self.entry_type )
        return qs

#    class Media:
#        js = ( 'js/menu-sort.js', 
#               )

class TypographyAdmin( BaseClass ):

    entry_type = 0 # Typography
    
class BookAdmin( BaseClass ):

    entry_type = 1 # Book

class NewsAdmin( BaseClass ):

    entry_type = 2 # News
    

#admin.site.register( Image )
admin.site.register( Book, BookAdmin ) 
admin.site.register( Typography, TypographyAdmin )
admin.site.register( News, NewsAdmin )

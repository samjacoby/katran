from django.contrib import admin
from django.forms import ModelForm
from entries.models import Image, Book, Typography, News, EntryRelationship


#class EntryForm( ModelForm ):
#    model = EntryRelationship
#    class = Media:
#        js = ( 'js/jquery-1.4.4.min.js',
#               'js/jquery-ui-1.8.9.custom.min.js',
#               'js/menu-sort.js', 
#               )


class EntryRelationshipInline( admin.StackedInline ):
    model = EntryRelationship
    fk_name = 'entry'
    extra = 0


class BaseClass( admin.ModelAdmin ):
    
    list_display = ('title', 'order')
    list_editable = ['order']
    exclude = ('order', 'entry_type')

    inlines = [ EntryRelationshipInline ]                                 

    def __unicode__(self):
        self.title

    def queryset(self, request):
        qs = super( BaseClass, self ).queryset(request)
        qs = qs.filter( entry_type=self.type )
        return qs

    class Media:
        js = ( 'js/jquery-1.4.4.min.js',
               'js/jquery-ui-1.8.9.custom.min.js',
               'js/menu-sort.js', 
               )

class TypographyAdmin( BaseClass ):

    type = 0 # Typography
    
class BookAdmin( BaseClass ):

    type = 1 # Book

class NewsAdmin( BaseClass ):

    type = 2 # News
    

admin.site.register( Image )
admin.site.register( Book, BookAdmin ) 
admin.site.register( Typography, TypographyAdmin )
admin.site.register( News, NewsAdmin )
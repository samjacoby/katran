from django.contrib import admin
from django.forms import ModelForm
from entries.models import Image, Book, Typography, News, EntryRelationship


class EntryRelationshipInline( admin.StackedInline ):
    model = EntryRelationship
    fk_name = 'entry'
    extra = 0


class BaseClass( admin.ModelAdmin ):
    inlines = [ EntryRelationshipInline ]                                 

    def queryset(self, request):
        qs = super( BaseClass, self ).queryset(request)
        qs = qs.filter( entry_type=self.type )
        return qs

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

from django.contrib import admin
from cms.admin.placeholderadmin import PlaceholderAdmin
from models import BookPlugin
from entries.models import Entry, Book, Typography


class BookPluginAdmin( admin.ModelAdmin ):
    def formfield_for_foreignkey( self, db_field, request, **kwargs ):
        if db_field == 'entry_type':
            kwargs['queryset'] = Entry.manager.get_all_of_type( 1 )
            return db_field.formfield(**kwargs)
        return super( BookPluginAdmin, self).formfield_for_foreignkey( db_field, request, **kwargs )


#admin.site.register(BookPlugin, BookPluginAdmin)


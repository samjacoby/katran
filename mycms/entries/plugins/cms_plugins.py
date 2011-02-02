from cms.models import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from entries.models import Entry, Book
from entries.plugins.models import BookPlugin as BookPluginModel
from entries.plugins.models import IndexPicture as IndexPictureModel


class EntryList( CMSPluginBase ):

    def render( self, context, instance, placeholder ):
        l = Entry.manager.get_all_of_type( self.type )
        context.update( { 'list': l } )
        return context

class TypographyList( EntryList ):

    type = 0 # Typography
    name = 'Typography Index'
    render_template = 'entries/plugins/book_list.html'

class BookList( EntryList ):

    type = 1 # Books
    name = 'Book Index'
    render_template = 'entries/plugins/book_list.html'

class NewsList( EntryList ):

    type = 2 # News
    name = 'News Index'
    render_template = 'entries/plugins/book_list.html'


class BookPlugin( CMSPluginBase ):
    model = BookPluginModel
    name = 'Book Plugin'
    render_template = 'entries/plugins/book.html'

    def render( self, context, instance, placeholder):
        context.update( {'instance':instance} )
        return context

class IndexPicturePlugin( CMSPluginBase ):
    model = IndexPictureModel
    name = 'Index Picture'
    render_template = 'cms/plugins/picture.html'

    def render( self, context, instance, placeholder ):
        context.update( {'instance':instance} )
        return context


plugin_pool.register_plugin( BookPlugin )
plugin_pool.register_plugin( TypographyList )
plugin_pool.register_plugin( BookList )
plugin_pool.register_plugin( NewsList )
plugin_pool.register_plugin( IndexPicturePlugin )


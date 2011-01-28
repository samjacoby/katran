from cms.models import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from entries.models import Book
from entries.plugins.models import BookPlugin as BookPluginModel


class BookList( CMSPluginBase ):

    name = 'Book List'
    render_template = 'entries/plugins/book_list.html'

    def render( self, context, instance, placeholder):
        l = Book.objects.all()
        context.update( {'list':l} )
        return context

class BookPlugin( CMSPluginBase ):
    model = BookPluginModel
    name = 'Book Plugin'
    render_template = 'entries/plugins/book.html'

    def render( self, context, instance, placeholder):
        context.update( {'instance':instance} )
        return context

plugin_pool.register_plugin(BookPlugin)
plugin_pool.register_plugin(BookList)


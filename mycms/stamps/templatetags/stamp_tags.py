from django import template
from classytags.arguments import IntegerArgument, Argument
from classytags.core import Options
from classytags.helpers import InclusionTag
from menus.menu_pool import menu_pool

register = template.Library()        

class ShowAttrMenu( InclusionTag ):
    name = 'stamp_menu'
    template = 'menu/test.html'

    options = Options(
        Argument('name', default=None, required=False),
        Argument('template', default='menu/test.html', required=False),
    )                                          

    def get_context(self, context, template, name ):
        try:
            request = context['request']
        except KeyError:
            return { 'template': 'menu/empty.html' }
        
        nodes = menu_pool.get_nodes(request)
        nodes = menu_pool.get_nodes_by_attribute( nodes, 'type', name )

        try:
            context = { 'children': nodes }

        except:
            context = { 'template': template}
            
        return context
register.tag( ShowAttrMenu )

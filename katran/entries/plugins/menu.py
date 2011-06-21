from cms.menu_bases import CMSAttachMenu
from menus.base import Menu, NavigationNode, Modifier
from menus.menu_pool import menu_pool
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from entries.models import Entry, Book, Typography

class BookMenu(CMSAttachMenu):
    name = _("Books Menu") # give the menu a name, this is required.

    def get_nodes(self, request):
        """
        This method is used to build the menu tree.
        """
        nodes = []
        namespace = 'book'
        for book in Book.manager.get_all_books():
            node = NavigationNode(
                book.order,                                          
                '/%s%s' % ('books', 
                            reverse('book_detail', 
                                    urlconf='entries.urls.books', 
                                    args=[book.order])),
                book.order,
                parent_namespace=namespace,
                attr={'type':'book'}
            )
            try:
                node.prev = nodes[-1]
                nodes[-1].next = node
            except IndexError:
                pass
            nodes.append(node)
        return nodes
menu_pool.register_menu(BookMenu) # register the menu.


class TypographyMenu(CMSAttachMenu):
    name = _("Typography Menu") # give the menu a name, this is required.

    def get_nodes(self, request):
        """
        This method is used to build the menu tree.
        """
        nodes = []
        namespace = 'typography'
        for typography in Typography.manager.get_all_typography():
            node = NavigationNode(
                typography.order,                                          
                '/%s%s' % ( 'typography', 
                            reverse('typography_detail', 
                                    urlconf='entries.urls.typography', 
                                            args=[ typography.order])),
                typography.order,
                parent_namespace=namespace,
                attr={'type':'typography'}
            )
            try:
                node.prev = nodes[-1]
                nodes[-1].next = node
            except IndexError:
                pass
            nodes.append(node)
        return nodes
menu_pool.register_menu(TypographyMenu) # register the menu.

# This should be used to mark the next and previous. Then that gets pulled out 
# by a templatetag. How's that sound?
class EntryModifier(Modifier):
    """Menu Modifier for entries,
    hide the MenuEntry in navigation, not in breadcrumbs"""

    def modify(self, request, nodes, namespace, root_id, post_cut, breadcrumb):
        """Modify nodes of a menu"""
        if breadcrumb:
            return nodes
        for node in nodes:
            if node.attr.get('selected'):
                node.next_link = 'what'
                selected_index = nodes.index(node)
#               nodes.remove(node)
        return nodes

#menu_pool.register_modifier(EntryModifier)

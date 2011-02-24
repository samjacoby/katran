from menus.base import Menu, NavigationNode
from menus.menu_pool import menu_pool
from cms.menu_bases import CMSAttachMenu
from stamps.models import Designer, Family, Stamp

class DesignerMenu( CMSAttachMenu ):
    name = "Designer Menu"
    def get_nodes(self, request):
        nodes = []
        for e in Designer.objects.filter(is_published=True, in_navigation=True):
            nodes.append(NavigationNode(e.display_name, 'designer', e.pk))
        return nodes

class FamilyMenu( CMSAttachMenu ):
    name = "Family Menu"
    def get_nodes(self, request):
        nodes = []
        for e in Family.objects.filter(is_published=True, in_navigation=True):
            nodes.append(NavigationNode(e.order, 'families', e.pk))
        return nodes

class StampMenu( CMSAttachMenu ):
    name = "Stamp Menu"
    def get_nodes(self, request):
        nodes = []
        for e in Stamp.objects.filter(is_published=True, in_navigation=True):
            nodes.append(NavigationNode(e.order, 'stamp', e.pk))
        
        return nodes

menu_pool.register_menu(DesignerMenu)
menu_pool.register_menu(FamilyMenu)
menu_pool.register_menu(StampMenu)
    

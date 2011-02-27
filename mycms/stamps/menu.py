from menus.base import Menu, NavigationNode
from menus.menu_pool import menu_pool
from cms.menu_bases import CMSAttachMenu
from stamps.models import Designer, Family, Stamp


class StampMenu(CMSAttachMenu):
    name = "Stamp Menu"
    def get_nodes(self, request):

        nodes = []
        namespace = 'stamp'
        
        for d in Designer.objects.select_related('families', 'stamps').filter(is_published=True, in_navigation=True):
            designer_key = '%s' % d.normalized_name
            designer_node = NavigationNode(d.display_name, d.get_absolute_url(), designer_key, parent_namespace=namespace)
            nodes.append(designer_node)
        
            for f in Family.objects.filter(is_published=True, in_navigation=True).filter(designer = d):
                family_key = '%s-%s' % (designer_key, f.order)
                family_node = NavigationNode(f.order, f.get_absolute_url(), family_key, designer_key, parent_namespace=namespace)
                nodes.append(family_node)
        
                for s in Stamp.objects.filter(is_published=True, in_navigation=True).filter(family = f):
                    stamp_key = '%s-%s' % (family_key, s.order)
                    nodes.append(NavigationNode(s.order, s.get_absolute_url(), stamp_key, family_key, parent_namespace=namespace))
        
        return nodes
                    
menu_pool.register_menu(StampMenu)
    

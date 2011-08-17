from menus.base import Menu, NavigationNode
from menus.menu_pool import menu_pool
from cms.menu_bases import CMSAttachMenu
from stamps.models import Designer, Family, Stamp


class StampMenu(CMSAttachMenu):
    name = "Stamp Menu"
    def get_nodes(self, request):

        nodes = []
        stamps = []
        families = []
        namespace = 'stamp'
        
        for d in Designer.cobjects.list():
            designer_key = '%s' % d.normalized_name
            designer_node = NavigationNode(d.name, 
                                           d.get_absolute_url(), 
                                           designer_key,
                                           parent_namespace=namespace,
                                           attr={'type':'designer', 'stamp_type': d.stamp_type})
            nodes.append(designer_node)
        
            for f in Family.objects.filter(is_published=True, 
                                           in_navigation=True,
                                           designer = d):
                family_key = '%s-%s' % (designer_key, f.order)
                family_node = NavigationNode(f.order, 
                                             f.get_absolute_url(), 
                                             family_key, 
                                             designer_key, 
                                             parent_namespace=namespace,
                                             attr={'type':'family'})
                try:
                    family_node.next = None
                    family_node.prev = families[-1]
                    families[-1].next = family_node
                except IndexError:
                    family_node.prev = None
                families.append(family_node)
        
                for s in Stamp.objects.filter(is_published=True, 
                                              in_navigation=True, 
                                              family = f):
                    stamp_key = '%s-%s' % (family_key, s.order)
                    stamp_node = NavigationNode(
                            s.order, 
                            s.get_absolute_url(), 
                            stamp_key, 
                            family_key, 
                            parent_namespace=namespace,
                            attr={'type':'stamp', 'value':s.value})
                    try:
                        stamp_node.next = None
                        stamp_node.prev = stamps[-1]
                        families[-1].next = stamp_node
                    except IndexError:
                        stamp_node.prev = None
                    stamps.append(stamp_node)
        
        nodes.extend(families)
        nodes.extend(stamps)
        return nodes
                    
menu_pool.register_menu(StampMenu)
    

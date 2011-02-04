from django import template
from classytags.arguments import IntegerArgument, Argument
from classytags.core import Options
from classytags.helpers import InclusionTag
from menus.menu_pool import menu_pool

register = template.Library()        

def cut_after(node, levels, removed):
    """
    given a tree of nodes cuts after N levels
    """
    if levels == 0:
        removed.extend(node.children)
        node.children = []
    else:
        for n in node.children:
            cut_after(n, levels - 1, removed)

def remove(node, removed):
    removed.append(node)
    if node.parent:
        if node in node.parent.children:
            node.parent.children.remove(node)

def cut_levels(nodes, from_level, to_level, extra_inactive, extra_active):
    """
    cutting nodes away from menus
    """
    final = []
    removed = []
    selected = None
    for node in nodes: 
        if not hasattr(node, 'level'):
            # remove and ignore nodes that don't have level information
            remove(node, removed)
            continue
        if node.level == from_level:
            # turn nodes that are on from_level into root nodes
            final.append(node)
            node.parent = None
        if not node.ancestor and not node.selected and not node.descendant:
            # cut inactive nodes to extra_inactive, but not of descendants of 
            # the selected node
            cut_after(node, extra_inactive, removed)
        if node.level > to_level and node.parent:
            # remove nodes that are too deep, but not nodes that are on 
            # from_level (local root nodes)
            remove(node, removed)
        if node.selected:
            selected = node
        if not node.visible:
            remove(node, removed)
    if selected:
        cut_after(selected, extra_active, removed)
    if removed:
        for node in removed:
            if node in final:
                final.remove(node)
    return final

def get_second_level_menu_linkss( selected_node ):
    current_index = selected_node.parent.children.index(selected_node)
    try:
        next = selected_node.children[current_index + 1]
    except IndexError:
        next = None
    try:
        prev = selected_node.children[current_index - 1]
    except IndexError:
        prev = None

    return { 'next':next, 'prev':prev }

def get_second_level_menu_links( selected_node ):
    current_index = selected_node.parent.children.index(selected_node)
    try:
        next = selected_node.children[current_index + 1]
    except IndexError:
        next = None
    try:
        prev = selected_node.children[current_index - 1]
    except IndexError:
        prev = None

    return { 'next':next, 'prev':prev }
register.inclusion_tag('menu/menu_links.html')(get_second_level_menu_links)


def get_top_level_menu_links( nodes ):  
    ''' This is nice, because it doesn't call any queries.'''    
    current_index = 0
    for node in nodes:
        if node.selected:
            current_index = nodes.index(node)

    try:
        next = nodes[current_index + 1]
    except IndexError:
        next = None
    try:
        prev = nodes[current_index - 1]
    except IndexError:
        prev = None
    
    # A negative index wraps around, so do a manual check here, to avoid that.
    if current_index is 0:
        prev = None

    return { 'next': next, 'prev': prev }

register.inclusion_tag('menu/menu_links.html')(get_top_level_menu_links)

from entries.models import Entry

def get_next_prev_nav( element, nodes ):

    links = get_next_prev( nodes )

    # Get total order to compare it to current element.
    max_order = Entry.manager.get_all_of_type( element.entry_type ).count()
    
    # Otherwise, we're somewhere in the middle of list, and should increment order.
    if element.entry_type == 0:
        prev = '/%s/%s/' % ('typography', element.order - 1)
        next = '/%s/%s/' % ('typography', element.order + 1)
    elif element.entry_type == 1:
        prev = '/%s/%s/' % ('books', element.order - 1)
        next = '/%s/%s/' % ('books', element.order + 1)
 
 # Just use original index, if we're at the beginning or the end of something.
    if element.order == max_order: # we're at the end of the list
        next = links['next']          
    elif element.order == 1: # we're at the beginning of the list
        prev = links['prev']
    return {
        'next': next,
        'prev': prev,
    }
register.inclusion_tag('menu/next_link.html')(get_next_prev_nav)

def find_ancestor( node ):
    if hasattr(node, 'selected'):
        return node
    if node.parent:
        result = find_selected(node.children)
        if result:
            return result

class SSubNav( InclusionTag ):
    name = 'sub_nav'
    template = 'menu/dummy.html'

    options = Options(                     
            IntegerArgument('levels', default=2, required=False),
            Argument('template', default='menu/sub_menu.html', required=False))
            
    def get_context(self, context, levels, template):
        try:
            request = context['request']
        except KeyError:
            return { 'template': 'menu/empty.html' }

        nodes = menu_pool.get_nodes( request )
        children = []
        
        for node in nodes:
            if node.selected:
                cut_after( node, levels, [])
                cut_after(node, levels, [])
                children = node.children
                for child in children:
                    child.parent = None
                children = menu_pool.apply_modifiers(children, request, post_cut=True)
        
        for child in nodes:
            if child.selected or child.ancestor:
                current_index = nodes.index(node)
        try:
            next = children[current_index + 1]
        except IndexError:
            next = None
        try:
            prev = children[current_index - 1]
        except IndexError:
            prev = None
        
        if current_index is 0:
            prev = None

        try:
            context.update ({ 'next': next, 'prev': prev })
        except:
            pass

        children = nodes

        context.update({ 'children':children, 'template':template })
        return context

class SubMenu(InclusionTag):
    """
    show the sub menu of the current nav-node.
    -levels: how many levels deep
    -temlplate: template used to render the navigation
    """
    name = 'show_sub'
    template = 'menu/dummy.html'
    
    options = Options(
        IntegerArgument('levels', default=100, required=False),
        Argument('template', default='menu/sub_menu.html', required=False),
    )
    
    def get_context(self, context, levels, template):
        try:
            # If there's an exception (500), default context_processors may not be called.
            request = context['request']
        except KeyError:
            return {'template': 'menu/empty.html'}
        nodes = menu_pool.get_nodes(request)
        
        
        for node in nodes:
            if node.selected or node.ancestor:
                current_index = nodes.index(node)

        try:
            next = nodes[current_index + 1]
        except IndexError:
            next = None
        try:
            prev = nodes[current_index - 1]
        except IndexError:
            prev = None
        #nodes = cut_levels(nodes, from_level, to_level, extra_inactive, extra_active)
        
        # A negative index wraps around, so do a manual check here, to avoid that.
        if current_index is 0:
            prev = None

        try:
            context.update ({ 'template': template, 'next': next, 'prev': prev })
        except:
            pass
        
        
        children = []
        for node in nodes:
            if node.selected:
                cut_after(node, levels, [])
                children = node.children
                for child in children:
                    child.parent = None
                children = menu_pool.apply_modifiers(children, request, post_cut=True)

        context.update({
            'children':False,
            'template':template,
            'from_level':0,
            'to_level':0,
            'extra_inactive':0,
            'extra_active':0
        })
        return context        
register.tag(SubMenu)


class TopNav( InclusionTag ):
    name = 'top_nav'
    template = 'menu/dummy.html'

    options = Options(
        IntegerArgument('from_level', default=0, required=False),
        IntegerArgument('to_level', default=1, required=False),
        Argument('template', default='menu/menu.html', required=False),
        Argument('namespace', default=None, required=False),
        Argument('root_id', default=None, required=False),
    )

    def get_context(self, context, template, from_level, to_level,  root_id, namespace ):
        try:
            request = context['request']
        except KeyError:
            return { 'template': 'menu/empty.html' }
        
        nodes = menu_pool.get_nodes( request, namespace, root_id )
        
        current_index = False
        final = []
        
        extra_inactive = 0
        extra_active = 1000
        for node in nodes:        
            if not node.visible:
                nodes.remove(node)
        nodes = cut_levels(nodes, from_level, to_level, extra_inactive, extra_active)
        nodes = menu_pool.apply_modifiers(nodes, request)

        for node in nodes:
            if node.selected or node.ancestor:
                current_index = nodes.index(node)

        try:
            next = nodes[current_index + 1]
        except IndexError:
            next = None
        try:
            prev = nodes[current_index - 1]
        except IndexError:
            prev = None
        #nodes = cut_levels(nodes, from_level, to_level, extra_inactive, extra_active)
        
        # A negative index wraps around, so do a manual check here, to avoid that.
        if current_index is 0:
            prev = None

        try:
            context.update ({ 'c': current_index, 'top_next': next, 'top_prev': prev })
        except:
            pass

        children = nodes

        try:
            context.update ({ 'children': children,
                              'template': template,
                              'namespace': namespace })
        except:
            context = { 'template': template }
        return context

register.tag( TopNav )




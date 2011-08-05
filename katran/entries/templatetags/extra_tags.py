from django import template
from classytags.arguments import IntegerArgument, Argument
from classytags.core import Options
from classytags.helpers import InclusionTag
from menus.menu_pool import menu_pool

register = template.Library()        

class PrevNext( InclusionTag ):
    name = 'prev_next_links'
    template = 'menu/prev_next_links.html'

    options = Options(
        IntegerArgument('from_level', default=0, required=False),
        IntegerArgument('to_level', default=1, required=False),
        Argument('template', default='menu/prev_next_links.html', required=False),
        Argument('namespace', default=None, required=False),
        Argument('root_id', default=None, required=False),
    )

    def get_context(self, context, template, from_level, to_level,  root_id, namespace ):
        try: 
            try:
                request = context['request']
            except KeyError:
                return { 'template': 'menu/empty.html' }
            
            nodes = menu_pool.get_nodes( request, namespace, root_id )
            current_index = None
            
            root_nodes = []
            for node in nodes:
                if node.level == 0:
                    root_nodes.append(node)
            for node in root_nodes:
                assert node.level == 0 # There should be only root level nodes
                if node.selected or node.ancestor: 
                    current_index = root_nodes.index(node)
                    assert current_index != None
                    break

            # This is done after selection, as the selected node can be invisible
            for n in root_nodes:
                # Cut out any invisible nodes (this could have weird behavior)
                if not n.visible:
                    root_nodes.remove(n)
            
            try: # Next Link
                next_link = root_nodes[current_index + 1]
            except IndexError:
                next_link = None
            try: # Previous Link
                prev_link = root_nodes[current_index - 1]
                if current_index == 0:
                    raise IndexError
            except IndexError:
                prev_link = None

            try:
                context = {'next': next_link, 'prev': prev_link}

            except:
                context = { 'template': template}
                
            return context
        except Exception, e:
            pass
register.tag( PrevNext )

def get_next_sibling(node, nodes):
    """Fetch the nearest sibling of node, or return nothing."""
    try:
        if node.parent:
            next = node.parent.children[node.parent.children.index(node) + 1]
            return next
        else:
            i = nodes.index(node) + 1
            next = nodes[i]
            while next.level != 0:
                i = i + 1
                next = nodes[i]

            if next.level == 0:
                return next 
        
        return None
    except IndexError, AttributeError:
        return None

def get_prev_sibling(node, nodes):
    """Return the most recent previous sibling of a given node, or nothing."""
    try:
        # If there's a parent, grab the sibling from the tree
        if node.parent:
            index = node.parent.children.index(node) - 1
            prev = node.parent.children[index]
            if index < 0:
                # This is the first child, so return parent
                return node.parent
            else:
                return prev
        else:
            # We're at the top-level, so grab the previous sibling by level
            i = nodes.index(node)                   
            for prev in reversed(nodes[:i]):
                if prev.level == 0:
                    return prev 
        return None
    except IndexError:
        return None

def get_last_child(node):
    """Fetch the last child of a node (with children)."""
    try:
        if node.children:
            return node.children[-1]
        return None
    except IndexError:
        return None

def get_next_parent(node, nodes):
    """Fetch a node's parent's next sibling"""
    node = node.parent
    next = None 
    while not next:
        next = get_next_sibling(node, nodes)
        if not next:
            next = get_next_parent(node, nodes)
    
    return next

class PrevNextInternal(InclusionTag):

    """Fetch the next & previous page on the site, according to some rules."""

    name = 'prev_next_links_internal'
    template = 'menu/prev_next_links_internal.html'

    options = Options(
        IntegerArgument('from_level', default=0, required=False),
        IntegerArgument('to_level', default=1, required=False),
        Argument('template', default='menu/prev_next_links.html', required=False),
        Argument('namespace', default=None, required=False),
        Argument('root_id', default=None, required=False),
    )

    def get_context(self, context, template, from_level, to_level,  root_id, namespace ):
        try:
            request = context['request']
        except KeyError:
            return { 'template': 'menu/empty.html' }
        
        nodes = menu_pool.get_nodes( request, namespace, root_id )
        
        current_index = None

        for node in nodes:
            if node.selected: # There should always be a selected node
                current_index = nodes.index(node)
                break

        for n in nodes:
            if not n.visible:
                nodes.remove(n)

#        if hasattr(node, 'next') and hasattr(node, 'prev'):
#            context = { 'index':current_index, 'level':node.next, 'sub_next': node.next, 'sub_prev': node.prev }
#            return context                      
            
        # Handle index pages and intermediary pages with children
        print node.title
        print node.children
        
        if node.children: 
            try: # Next Link
                next_link = node.children[0] # The next one is the first
            except IndexError:
                next_link = None
            try: # Previous Link
                prev_link = get_prev_sibling(node, nodes)
                if prev_link != None and prev_link.level == node.level:
                    prev_link_child = get_last_child(prev_link)
                    if prev_link_child:
                        prev_link = prev_link_child
            except IndexError:
                prev_link = None
        # We're at a childrenless page, an index or a leaf
        else: 
            try: # Next Link
                next_link = get_next_sibling(node, nodes)
                if not next_link and node.parent:
                    next_link = get_next_parent(node, nodes)
            except:
                next_link = None
            try: # Prev Link                                    
                prev_link = get_prev_sibling(node, nodes) 
                if prev_link != None and prev_link.level == node.level:
                    prev_link_child = get_last_child(prev_link)
                    if prev_link_child:
                        prev_link = prev_link_child
            except IndexError:
                prev_link = None
        
        try:
            context = { 'index':current_index, 'level':node.children, 'sub_next': next_link, 'sub_prev': prev_link }

        except:
            context = { 'template': template}
            
        return context
register.tag( PrevNextInternal )

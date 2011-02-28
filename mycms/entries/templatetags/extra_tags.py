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
            request = context['request']
        except KeyError:
            return { 'template': 'menu/empty.html' }
        
        nodes = menu_pool.get_nodes( request, namespace, root_id )
        
        current_index = None
        
        for node in nodes:
            if node.level != 0: # We're only interested in root-level nodes
                nodes.remove(node)
            
        for node in nodes:
            if node.selected or node.ancestor: # If we're at root, this is okay
                current_index = nodes.index(node)
                break
        
        for n in nodes:
            if not n.visible:
                nodes.remove(n)
        
        try:
            next_link = nodes[current_index + 1]
            i = current_index + 2
            while next_link.level != node.level: # We're not at the top level
                next_link = nodes[i]
                i = i + 1
        except IndexError:
            next_link = None
        try:
            prev_link = nodes[current_index - 1]
            if prev_link.level != 0:
                prev_link = None
        except IndexError:
            prev_link = None
        
        if current_index == 0:
            prev_link = None 

        try:
            context = {  'index': current_index, 'selected': node,'next': next_link, 'prev': prev_link }

        except:
            context = { 'template': template}
            
        return context
register.tag( PrevNext )


class PrevNextInternal( InclusionTag ):
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
            if node.selected:# or node.ancestor:
                current_index = nodes.index(node)
                break

        assert current_index != None

        for n in nodes:
            if not n.visible:
                nodes.remove(n)
        
        # Handle index pages and intermediary pages with children
        if node.children: 
            try:
                next_link = node.children[0] # The next one is the first
                assert next_link.level != node.level
                if next_link.level > node.level and next_link.level >= 2:
                    while next_link.children:
                        next_link = next_link.children[0]
                #V
                #   next_link = nodes[current_index + 1] # Next root level item
                #   if next_link.level != node.level: # Non-sequential indices
                ##      next_link = None
                #    assert next_link.level == 0 or next_link == None
            except IndexError:
                next_link = None
            try:
                prev_link = nodes[current_index - 1]
                while prev_link.children:
                    prev_link = prev_link.children[-1]
            except IndexError:
                prev_link = None
        # We're at a childrenless page, an index or a leaf
        else: 
            try:
                next_link = nodes[current_index + 1]
                if next_link.level != node.level or next_link.parent_namespace != node.parent_namespace:
                    if not node.parent:
                        next_link = None
                    else:
                        next_link =  nodes[nodes.index(node.parent) + 1]
            except IndexError:
                # No next page. Check for parents or end-of-tree.
                if node.parent:
                    next_link = node.parent
                    while next_link.parent:
                        next_link = next_link.parent
                else:
                    next_link = None
            try:
                prev_link = nodes[current_index - 1]
                if prev_link.level != node.level:
                    if node.parent:
                        prev_link = node.parent
                        while prev_link.parent:
                            prev_link = prev_link.parent
                    else:
                        prev_link = None
                else:
                    while prev_link.children:
                        prev_link = prev_link.children[-1]
           #    if prev_link.level != node.level or prev_link.parent_namespace != node.parent_namespace:
           #        if node.parent:
           #            prev_link = node.parent
           #            while prev_link.parent:
           #                prev_link = prev_link.parent
           #        else:
           #            prev_link = node
           #    else:
           #       while prev_link.children:
           #           prev_link = prev_link.children[-1]
            except IndexError:
                prev_link = None
        
        try:
            context = { 'index':current_index, 'level':node.parent_namespace, 'sub_next': next_link, 'sub_prev': prev_link }
        except:
            context = { 'template': template}
            
        return context
register.tag( PrevNextInternal )

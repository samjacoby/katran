from django import template
from classytags.arguments import IntegerArgument, Argument
from classytags.core import Options
from classytags.helpers import InclusionTag
from menus.menu_pool import menu_pool

register = template.Library()        

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

class PrevNextFamily( InclusionTag ):
    '''Previous and next links that iterate over stamp families'''

    name = 'stamp_family_links'
    template = 'menu/prev_next_links.html'

    options = Options(
        IntegerArgument('family', default=1, required=False),
        Argument('namespace', default=None, required=False),
        Argument('root_id', default=None, required=False),
    )

    def get_context(self, context, family,  root_id, namespace ):
        try:
            request = context['request']
        except KeyError:
            return { 'template': 'menu/empty.html' }
        
        # Fetch all nodes of all types
        all_nodes = menu_pool.get_nodes(request, namespace, root_id )
        # Fetch families
        nodes = menu_pool.get_nodes_by_attribute(all_nodes, 'type', 'family')

        current_index = None

        for node in nodes:
            if node.descendant:
                if node.parent.attr['type'] == 'designer': 
                    # We're the designer level, so make first descendant
                    current_index = nodes.index(node)
                    break
                else:
                    # We're at the root index, so just return with first family and arbitrary previoous
                    context['next'] = nodes[0]
                    context['prev'] = node.parent.parent.parent # This happens to be /resources/
                    return context
            if node.selected or node.ancestor:
                current_index = nodes.index(node)
                break

        assert current_index != None

        # This is done after selection, as the selected node can be invisible
        for n in nodes:
            # Cut out any invisible nodes (this could have weird behavior)
            if not n.visible:
                nodes.remove(n)
        
        try:
            next_link = nodes[current_index + 1]
        except IndexError:
            next_link = (node.parent).parent
        prev_link = nodes[current_index - 1]
        if current_index == 0:
            prev_link = (node.parent).parent


        context['next'] = next_link
        context['prev'] = prev_link

        return context                      
register.tag( PrevNextFamily )

class PrevNextStamp( InclusionTag ):
    '''Generate a link for the next viewable stamp'''
    name = 'stamp_links'
    template = 'menu/stamp_next.html'

    options = Options(
        Argument('namespace', default=None, required=False),
        Argument('root_id', default=None, required=False),
    )

    def get_context(self, context,  root_id, namespace ):
        try:
            request = context['request']
        except KeyError:
            return { 'template': 'menu/empty.html' }
        
        all_nodes = menu_pool.get_nodes(request, namespace, root_id )
        nodes = menu_pool.get_nodes_by_attribute(all_nodes, 'type', 'stamp')
        current_index = None
        
        for node in nodes:
            assert node.attr['type'] == 'stamp'

        for node in nodes:
            if node.selected or node.descendant:
                current_index = nodes.index(node)
                break

        assert current_index != None

        try:
            next_link = nodes[current_index + 1]
        except IndexError:
            next_link = ((node.parent).parent).parent
        context['next'] = next_link
        context['prev'] = None
        return context                      

register.tag( PrevNextStamp )

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

class StampFamilies( InclusionTag ):
    '''Generate a list of links to stamp families'''
    name = 'stamp_families'
    template = 'menu/stamp_links.html'

    options = Options(
        Argument('name', default=None, required=False),
        Argument('template', default='menu/test.html', required=False),
    )                                          

    def get_context(self, context, template, name ):
        try:
            request = context['request']
        except KeyError:
            return { 'template': 'menu/empty.html' }
        
        all_nodes = menu_pool.get_nodes(request)
        nodes = menu_pool.get_nodes_by_attribute( all_nodes, 'type', 'designer' )

        for node in all_nodes:
            # If we're at the root level, don't bother getting children
            if node.selected and node.level < 2:
                context = { 'template': template}
                return context
        
        for node in nodes:
            if node.selected and node.attr['type'] == 'designer':
                # Set first family to be selected
                node.children[0].selected = True
                break
            if node.ancestor and node.attr['type'] == 'designer':
                break

        try:
            context = { 'children': node.children }

        except:
            context = { 'template': template}
            
        return context
register.tag(StampFamilies)

class StampValues( InclusionTag ):
    '''Generate a linked list of stamp values'''
    name = 'stamp_values'
    template = 'menu/stamp_links_values.html'

    options = Options(
        Argument('name', default=None, required=False),
        Argument('template', default='menu/stamp_links.html', required=False),
    )                                          

    def get_context(self, context, template, name ):
        try:
            request = context['request']
        except KeyError:
            return { 'template': 'menu/empty.html' }
        
        all_nodes = menu_pool.get_nodes(request)
        nodes = menu_pool.get_nodes_by_attribute(all_nodes, 'type', 'family')

        for node in nodes:
            if (node.ancestor or node.selected) and node.attr['type'] == 'family':
                break
            if node.descendant: # We must be at a designer
                node.selected = True # This must be the first family, so select it
                break

        if node.selected: # We're at a family or designer, so automatically select the first stamp
          node.children[0].selected = True

        try:
            context = { 'children': node.children }
        except:
            context = { 'template': template}
            
        return context
register.tag( StampValues )

class DesignerMenu( InclusionTag ):
    '''A list of all available designers'''
    
    name = 'designer_menu'
    template = 'menu/designer_menu.html'

    options = Options(
        Argument('name', default=None, required=False),
        Argument('template', default='menu/stamp_links.html', required=False),
    )                                          

    def get_context(self, context, template, name ):
        try:
            request = context['request']
        except KeyError:
            return { 'template': 'menu/empty.html' }
        
        all_nodes = menu_pool.get_nodes(request)
        nodes = menu_pool.get_nodes_by_attribute( all_nodes, 'type', 'designer' )
        
        for node in nodes:
            if (node.ancestor or node.selected):
                node.selected = True # make sure this is true, as we'll use it in the templates
                break

        try:
            context = { 'children': nodes }
        except:
            context = { 'template': template}
            
        return context
register.tag( DesignerMenu )

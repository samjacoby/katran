from django import template
register = template.Library()

'''
def get_next_prevs( selected_node ):
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
'''

# This is really only good for Django-CMS pages and shouldn't be here, oh well.
def get_next_prev( nodes ):                                                   
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

    return { 
        'next': next, 
        'prev': prev 
    }

register.inclusion_tag('menu/next_link.html')(get_next_prev)

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
    # Index overrides
    if element.order == max_order: # we're at the end of the list
        next = links['next']          
    elif element.order == 1: # we're at the beginning of the list
        prev = links['prev']
    return {
        'next': next,
        'prev': prev,
    }
register.inclusion_tag('menu/next_link.html')(get_next_prev_nav)



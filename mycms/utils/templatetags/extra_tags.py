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
    
    # A negative index wraps around, so do a manual check here.
    if current_index is 0:
        prev = None

    return { 
        'next': next, 
        'prev': prev 
    }

register.inclusion_tag('menu/next_link.html')(get_next_prev)


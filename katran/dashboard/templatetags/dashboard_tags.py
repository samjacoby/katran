from django import template

register = template.Library()        

@register.inclusion_tag('dashboard/includes/stamp_family.html', takes_context=True)
def render_stamps(context, index):
    '''Render a family of stamps'''
    return { 'stamps' : context['families'].nested[index] }

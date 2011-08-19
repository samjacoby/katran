from dbgettext.registry import registry, Options
from models import StampLink

class LinkOptions(Options):
    attributes = ('name', 'url', 'mailto')
    parent = 'page'

registry.register(StampLink, LinkOptions)

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from stamps.menu import DesignerMenu, FamilyMenu, StampMenu

class StampHook( CMSApp ):
    name = 'Stamp Application'
    urls = [ 'stamps.urls' ]
    menu = [ DesignerMenu, FamilyMenu, StampMenu ]

apphook_pool.register( StampHook )

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from stamps.menu import StampMenu

class StampHook( CMSApp ):
    name = 'Stamp Application'
    urls = [ 'stamps.urls' ]
    menu = [ StampMenu ]

apphook_pool.register( StampHook )

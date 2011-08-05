from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

class BookHook( CMSApp ):
    name = 'Book Application'
    urls = ['entries.urls.books']
#    menu = [BookMenu]

class TypographyHook( CMSApp ):
    name = 'Typography Application'
    urls = ['entries.urls.typography']
#    menu = [TypographyMenu]


apphook_pool.register( BookHook )
apphook_pool.register( TypographyHook )

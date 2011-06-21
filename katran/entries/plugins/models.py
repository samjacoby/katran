from django.db import models
from entries.models import Typography, Book, News                 
from django.utils.translation import ugettext_lazy as _
from cms.models import CMSPlugin

class IndexPicture( CMSPlugin ):
    """
    A custom picture which allows for index display (or not)
    """
    image = models.ImageField(_("image"), upload_to=CMSPlugin.get_media_path)
    display_in_index = models.BooleanField( default=0, help_text=_("if true, image will display in the corresponding index view"))
    url = models.CharField(_("link"), max_length=255, blank=True, null=True, help_text=_("if present image will be clickable"))
#    page_link = models.ForeignKey(Page, verbose_name=_("page"), null=True, blank=True, help_text=_("if present image will be clickable"))
    alt = models.CharField(_("alternate text"), max_length=255, blank=True, null=True, help_text=_("textual description of the image"))
    longdesc = models.CharField(_("long description"), max_length=255, blank=True, null=True, help_text=_("additional description of the image"))
    
    def __unicode__(self):
        if self.alt:
            return self.alt[:40]
        elif self.image:
            # added if, because it raised attribute error when file wasn't defined
            try:
                return u"%s" % basename(self.image.path)
            except:
                pass
        return "<empty>"

class BookPlugin( CMSPlugin ):
    book = models.ForeignKey('entries.Book', related_name='plugins')

    def __unicode__(self):
        return self.book.title


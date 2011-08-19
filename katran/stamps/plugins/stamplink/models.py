from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models import CMSPlugin

from stamps.models import Stamp

class StampLink(CMSPlugin):
    """
    A link to a stamp
    """
    name = models.CharField(_("name"), max_length=256)
    page_link = models.ForeignKey(Stamp, verbose_name=_("stamp"), blank=True, null=True)
    
    def __unicode__(self):
        return self.name

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse
from cms.models.fields import PlaceholderField


class ItemManager(models.Manager):
    
    def all_items(self):
        return self.objects.all()


class Sponsor(models.Model):
    '''
    This is a sponsor. Not much to see. Can be associated with anything.
    '''
    content_type = models.ForeignKey(ContentType)
    content_object = generic.GenericForeignKey()
    object_id = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=100)

    def __unicode__(self):                    
        return self.name


class DesignerManager(models.Manager):
def list(self): '''Return correctly ordered list of designers'''
        list = self.filter(is_published=True).filter(in_navigation=True).order_by('normalized_name').order_by('stamp_type')
        return list

class KModel(models.Model):

    is_published = models.BooleanField(default=True help_text='Published to live site?')
    in_navigation = models.BooleanField(default=True, help_text='Accessible through link in menu?')

    name = models.CharField(max_length=100, help_text='Displayed through-out the site')

    class Meta:
        abstract = True

    

class Designer(KModel):
    
    normalized_name = models.CharField( max_length=60, help_text='Normalized name for URL, e.g. Hermann Zapf becomes zapf.')
    DESIGNER_TYPE = (
            (0, 'Stamps'),
            (1, 'Other'),
            )
    
    # This should be done with tags
    stamp_type = models.IntegerField( 'Designer Menu Type', choices=DESIGNER_TYPE, default=0, help_text="Determines in which portion of the menu a designer is displayed.")

    info = PlaceholderField('designer_info')

    sponsor = generic.GenericRelation(Sponsor)

    objects = models.Manager()
    # Custom Manager
    cobjects = DesignerManager()
    
    def __unicode__(self):
        return self.display_name

    def get_absolute_url(self):
        return reverse('designer', 
                        kwargs = {'designer': self.normalized_name})

    class Meta:
        ordering = ['normalized_name']

class Family(KModel):
    designer  = models.ForeignKey(Designer, related_name='families')

    country = models.CharField(max_length=60, blank=True, help_text="If left blank, stamp's country will be used.")
    year = models.IntegerField(max_length=4, blank=True, null=True, help_text="If left blank, stamp's year will be used.")
    order = models.PositiveIntegerField( 'Order',  default=1 )                      
    sponsor = generic.GenericRelation(Sponsor)
    
    def __unicode__( self ):
        return "%s - %s" % (self.designer.display_name, self.name)

    def get_absolute_url(self):
        return reverse('stamps.views.detail', 
                        kwargs = {'designer': self.designer.normalized_name, 
                                  'family': self.order})
    class Meta:
        ordering = ['order']
        unique_together = ('designer', 'order')
        verbose_name_plural = 'Families'

class Stamp(KModel):
    family = models.ForeignKey(Family, related_name='stamps')
    url_override = models.CharField(max_length=40, blank=True, help_text="When set, this stamp will be accessible through this url.")

    country = models.CharField(max_length=60, blank=True, help_text="Will override stamp family country.")
    year = models.IntegerField(max_length=4, blank=True, null=True, help_text="Will override stamp family year.")
    value = models.CharField(max_length=50, blank=True)
    picture = models.ImageField(upload_to='stamps', blank=True, null=True)
    info = PlaceholderField('Stamp Info', related_name='stamp_info', help_text="Anything that should display immediately below the values of the stamps should go here.")
    footer = PlaceholderField('Stamp Footer', related_name='stamp_footer')

    # Order with which stamp appears in family
    order = models.PositiveIntegerField( 'Order',  default=1 )                      
    
    sponsor = generic.GenericRelation(Sponsor)

    def get_absolute_url(self):
        if self.url_override:
            return reverse('stamp-detail-url',
                kwargs = {'designer': self.family.designer.normalized_name, 
                          'family': self.family.order,
                          'stamp': self.order, 
                          'url_override':self.url_override})
            
        return reverse('stamps.views.detail', 
                        kwargs = {'designer': self.family.designer.normalized_name, 
                                  'family': self.family.order,
                                  'stamp': self.order })
    class Meta:
        ordering = ['order'] 
        unique_together = ('family', 'order')

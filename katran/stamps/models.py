from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse
from django.forms import ModelForm

from cms.models.fields import PlaceholderField
from menus.menu_pool import menu_pool

class ItemManager(models.Manager):
    
    def all_items(self):
        return self.objects.all()

class Sponsor(models.Model):
    '''
    This is a sponsor. Not much to see. Can be associated with anything.
    '''

    active = models.BooleanField(default=True, help_text='Active sponsor?')
    name = models.CharField(max_length=100)
    normalized_name = models.CharField(max_length=100, help_text='The text by which this sponsor is ordered')
    link = models.CharField(max_length=300)

    def __unicode__(self):                    
        return self.name

    class Meta:
        ordering = ['normalized_name'] 

class KModel(models.Model):

    is_published = models.BooleanField(default=True, help_text='Published to live site?')
    in_navigation = models.BooleanField(default=True, help_text='Accessible through link in menu?')

    name = models.CharField(max_length=100, help_text='Displayed through-out the site')
    sponsor  = models.ManyToManyField(Sponsor, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):

        # Invalidate the menu cache on creating/modifying objects
        menu_pool.clear(settings.SITE_ID, settings.LANGUAGE_CODE)
        
        super(KModel, self).save(*args, **kwargs)


class DesignerManager(models.Manager):

    def list(self): 
        return self.filter(is_published=True).filter(in_navigation=True).order_by('stamp_type', 'normalized_name')

    def ordered_list(self):
        return self.order_by('stamp_type', 'normalized_name')

class Designer(KModel):
    
    normalized_name = models.CharField( max_length=60, help_text='Normalized name for URL, e.g. Hermann Zapf becomes zapf.')
    DESIGNER_TYPE = (
            (0, 'Stamps'),
            (1, 'Other'),
            )
    
    # This should be done with tags
    stamp_type = models.IntegerField( 'Designer Menu Type', choices=DESIGNER_TYPE, default=0, help_text="Determines in which portion of the menu a designer is displayed.")

    info = PlaceholderField('designer_info')

    objects = models.Manager()
    # Custom Manager
    cobjects = DesignerManager()
    

    def get_absolute_url(self):
        return reverse('designer', 
                        kwargs = {'designer': self.normalized_name})

    class Meta:
        ordering = ['normalized_name']

class FamilyManager(models.Manager):

    def ordered_list(self): 
        return self.order_by('designer__normalized_name','order')


class Family(KModel):

    designer  = models.ForeignKey(Designer, related_name='families')
    country = models.CharField(max_length=60, blank=True, help_text="If left blank, stamp's country will be used.")
    year = models.IntegerField(max_length=4, blank=True, null=True, help_text="If left blank, stamp's year will be used.")
    order = models.PositiveIntegerField( 'Order',  default=1 )                      

    # Custom Manager
    objects = FamilyManager()
    
    def __unicode__( self ):
        return "%s - %s" % (self.designer.name, self.name)

    def get_absolute_url(self):
        return reverse('stamps.views.detail', 
                        kwargs = {'designer': self.designer.normalized_name, 
                                  'family': self.order})
    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Families'

class StampManager(models.Manager):

    def ordered_list(self): 
        return self.order_by('family__designer__normalized_name','family__order','order')

class Stamp(KModel):
    family = models.ForeignKey(Family, related_name='stamps')
    parent = models.ForeignKey('self', blank=True, null=True, help_text="Used in conjuction with URL override, to make one stamp accessible through another")
    url_override = models.CharField(max_length=40, blank=True, help_text="When set, this stamp will be accessible through this url.")

    country = models.CharField(max_length=60, blank=True, help_text="Will override stamp family country.")
    year = models.IntegerField(max_length=4, blank=True, null=True, help_text="Will override stamp family year.")
    value = models.CharField(max_length=50, blank=True)
    picture = models.ImageField(upload_to='stamps', blank=True, null=True)
    info = PlaceholderField('Stamp Info', related_name='stamp_info', help_text="Anything that should display immediately below the values of the stamps should go here.")
    footer = PlaceholderField('Stamp Footer', related_name='stamp_footer')

    # Custom Manager
    objects = StampManager()

    # Order with which stamp appears in family
    order = models.PositiveIntegerField( 'Order',  default=1 )                      

    def __unicode__( self ):
        return "%s - %s - %s. %s" % (self.family.designer.name, self.family.name, self.name, self.value)

    def get_absolute_url(self):
        # If this stamp is a child of another, append the URL to the parent stamp's URL
        if self.parent and self.url_override:
            return '%s%s' % (self.parent.get_absolute_url(), self.url_override)
        # If for whatever reason we just want to override the stamp URL, associate it with the family
        elif self.url_override:
            return reverse('stamp-detail-url',
                kwargs = {'designer': self.family.designer.normalized_name, 
                          'family': self.family.order,
                          'stamp': self.order, 
                          'url_override':self.url_override})
            
        # This is the regular view
        return reverse('stamps.views.detail', 
                        kwargs = {'designer': self.family.designer.normalized_name, 
                                  'family': self.family.order,
                                  'stamp': self.order })
    class Meta:
        ordering = ['order'] 

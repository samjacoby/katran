from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse
from cms.models.fields import PlaceholderField

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

class Designer(models.Model):
    
    
    display_name = models.CharField( max_length=60, blank=True, help_text='Designer name displayed in menus and elswhere.')
    normalized_name = models.CharField( max_length=60, help_text='Name for designer URL as well as alphabeticized listing.')
    DESIGNER_TYPE = (
            (0, 'Stamps'),
            (1, 'Other'),
            )
    
    stamp_type = models.IntegerField( 'Designer Menu Type', choices=DESIGNER_TYPE, default=0, help_text="Determines in which portion of the menu a designer is displayed.")

    is_published = models.BooleanField(help_text='Controls whether or not designer in published to site.')
    in_navigation = models.BooleanField(help_text='Whether or not designer appears in menus.')
    info = PlaceholderField('designer_info')

    sponsor = generic.GenericRelation(Sponsor)
    
    def __unicode__(self):
        return self.display_name
    def get_absolute_url(self):
        return reverse('stamps.views.detail', 
                        kwargs = {'designer': self.normalized_name})


    class Meta:
        ordering = ['normalized_name']

class Family(models.Model):
    designer  = models.ForeignKey(Designer, related_name='families')
    is_published = models.BooleanField(help_text='Controls whether or not family is published to site.')
    in_navigation = models.BooleanField(help_text='Whether or not family appears in menus.')
    name = models.CharField(max_length=100, help_text="Cannot be blank, but can be overriden by stamp name.")
    country = models.CharField(max_length=60, blank=True, help_text="If left blank, stamp's country will be used.")
    year = models.IntegerField(max_length=4, blank=True, null=True, help_text="If left blank, stamp's year will be used.")
    order = models.PositiveIntegerField( 'Order',  default=1 )                      
    sponsor = generic.GenericRelation(Sponsor)
    
    def __unicode__( self ):
        return self.name
    def get_absolute_url(self):
        return reverse('stamps.views.detail', 
                        kwargs = {'designer': self.designer.normalized_name, 
                                  'family': self.order})
    class Meta:
        ordering = ['-order']
        verbose_name_plural = 'Families'

class Stamp(models.Model):
    family = models.ForeignKey(Family, related_name='stamps')
    is_published = models.BooleanField(help_text='Controls whether or not stamp is published to site.')
    in_navigation = models.BooleanField(help_text='Whether or not stamp appears in menus.')
    url_override = models.CharField(max_length=40, blank=True, help_text="When set, this stamp will be accessible <em>only</em> through this url. In this case, order will be ignored. The url cannot be a number but can be nested.")
    name = models.CharField(max_length=100, blank=True, help_text="If entered, will override stamp family name.")
    country = models.CharField(max_length=60, blank=True, help_text="Will override stamp family country.")
    year = models.IntegerField(max_length=4, blank=True, null=True, help_text="Will override stamp family year.")
    value = models.CharField(max_length=30, blank=True)
    #picture = PlaceholderField('Stamp Image', related_name='stamp_picture', help_text="This container holds the stamp picture (and anything else in the same place)")
    picture = models.ImageField(upload_to='stamps', blank=True, null=True)
    info = PlaceholderField('Stamp Info', related_name='stamp_info', help_text="Anything that should display immediately below the values of the stamps should go here.")
    footer = PlaceholderField('Stamp Footer', related_name='stamp_footer')
    # Order with which stamp appears in family
    order = models.PositiveIntegerField( 'Order',  default=1 )                      
    
    sponsor = generic.GenericRelation(Sponsor)

    def get_absolute_url(self):
        return reverse('stamps.views.detail', 
                        kwargs = {'designer': self.family.designer.normalized_name, 
                                  'family': self.family.order,
                                  'stamp': self.order })
    class Meta:
        ordering = ['-order'] 

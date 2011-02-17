from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.forms import ModelForm
from django.utils.safestring import mark_safe

class DesignerManager(models.Manager):

    # The model class for this manager is always available as 
    # self.model, but in this example we are only relying on the 
    # filter() method inherited from models.Manager.
    def get_stamps(self):
         self.families()


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

class Footer(models.Model):
    '''
    This is a footer. It's a block of text that can go anywhere.
    '''
    content_type = models.ForeignKey(ContentType)
    content_object = generic.GenericForeignKey()
    object_id = models.PositiveIntegerField()
    footer = models.TextField("Footers")


class Designer(models.Model):
    '''
    Describes a designer. Very interesting.
    '''
    def __unicode__(self):
        return self.name

    def _get_full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.first_name, self.last_name)
    _get_full_name.admin_order_by = 'last_name'

    def get_absolute_url(self):
            return "/stamps/%s/" % self.last_name_id
    
    name = property(_get_full_name)

    first_name = models.CharField(max_length=60, blank=True)
    last_name = models.CharField(max_length=60)
    # Denormalized last name. Used for ordering.
    last_name_id = models.CharField(max_length=60)
    bio = models.TextField("Biography", blank=True)
    bio.allow_tags = True
    sponsor = generic.GenericRelation(Sponsor)
    
    LINK_CLASS = (
        (0, 'Stamp Designer'),
        (1, 'Other Designer'),
        (2, 'Something Else'),
        )
    designer_class = models.IntegerField("Designer Type", max_length=1, choices=LINK_CLASS, default=0)
    class Meta:
        ordering = ('last_name_id',)
 
class Typeface(models.Model):
    name = models.CharField(max_length=100)
    designer = models.ForeignKey(Designer)                                           
    typeface_img = models.FilePathField("Typeface Image", path=settings.STATIC_ROOT, recursive=True, blank=True)
    def __unicode__(self):                    
        return self.name

class StampFamily(models.Model):
    '''
    This is not a stamp. It is a family of stamps.
    '''

    designer = models.ForeignKey(Designer, related_name='families')
    name = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=50, blank=True)
    year = models.IntegerField(max_length=4, blank=True, null=True)
    footer = generic.GenericRelation(Footer)
    sponsor = generic.GenericRelation(Sponsor)
    order = models.IntegerField("Family Number", blank = True, null = True)

    def __unicode__(self):
        return "%s: %s" % (self.designer.name, self.name)

    def get_absolute_url(self):
        return "%s%s/" % (self.designer.get_absolute_url(), self.order)
    
    class Meta:
        ordering = ('order',)
        verbose_name_plural = 'Stamp Families'

class StampManager(models.Manager):

    def first(self):
        return self.all().order_by('stamp_family__designer__designer_class','stamp_family__designer__last_name_id','stamp_family__order','order')[0]

class Stamp(models.Model):
    '''
    This is a stamp. This is the last leaf. It's got the picture and is 
    associated with a stamp family.
    '''
    def __unicode__(self):
        return '%s: %s (%s)' % (self.stamp_family.designer, 
                self.stamp_family.name, self.name)
    def get_absolute_url(self):
        return '%s%s/' % (self.stamp_family.get_absolute_url(), self.order)
    stamp_family = models.ForeignKey(StampFamily, related_name='stamps')

    # Used in admin list_display for thumbnails.
    def admin_image(self):
        return '<img height="200" src="%s%s"/>' % (settings.STATIC_URL, self.img)
    admin_image.allow_tags = True

    # Custom stamp manager
    get_stamp = StampManager()
    # Make standard manager methods available
    objects = models.Manager()

    name = models.CharField("Stamp Name", max_length=100, blank=True)
    value = models.CharField(max_length=50, blank=True)
    img = models.CharField("Stamp Image", max_length=100)
    order = models.IntegerField("Stamp Number", blank = True, null = True)
    
    sponsor = generic.GenericRelation(Sponsor) 
    footer = generic.GenericRelation(Footer)
    footer.allow_tags = True

    def __unicode__(self):
        return '%s: %s (%s)' % (self.stamp_family.designer, 
                self.stamp_family.name, self.name)
    def get_absolute_url(self):
        return '%s%s/' % (self.stamp_family.get_absolute_url(), self.order)
    stamp_family = models.ForeignKey(StampFamily, related_name='stamps')

    # Used in admin list_display for thumbnails.
    def admin_image(self):
        return '<img height="200" src="%s%s"/>' % (settings.STATIC_URL, self.img)
    admin_image.allow_tags = True
    # Build next and previous links.
    
    def get_link(self): 
        stamp_list = Stamp.objects.all().order_by('stamp_family__designer__designer_class','stamp_family__designer__last_name_id','stamp_family__order','order')
        found = False
        prev = None
        for i, stamp in enumerate(stamp_list, start=1):
            next = stamp
            if found:
                if not prev:
                    return {'next':next.get_absolute_url() }
                elif not next:
                    return {'prev':prev.get_absolute_url() }
                else:
                    return {'prev':prev.get_absolute_url(), 'next':next.get_absolute_url() }
            if stamp.id == self.id:
                found = True
                if i == len(stamp_list):
                    return {'prev':prev.get_absolute_url() }
            if not found:                   
                prev = stamp
    class Meta:
        ordering = ('order',)

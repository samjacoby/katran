from django.db import models
from django.core.urlresolvers import reverse
import os

class EntryManager( models.Manager ):

    def get_all_of_type(self, entry_type):
        return self.filter( entry_type=entry_type )

    def get_all_typography(self):
        return self.filter( entry_type=0 )

    def get_all_books(self):
        return self.filter( entry_type=1 )

    def get_all_news(self):
        return self.filter( entry_type=2 )

class Image( models.Model ):

    def __unicode__( self ):
        return self.title

    title = models.CharField( max_length=100 )
    src = models.ImageField( upload_to='images' )

class Entry( models.Model ):

    objects = models.Manager()
    manager = EntryManager()

    title = models.CharField( max_length=100 , blank=True )
    subtitle = models.CharField( max_length=100, blank=True ) 
    ENTRY_TYPE = (
            (0, 'Typography'),
            (1, 'Book'),
            (2, 'News'),
            )

    entry_type = models.IntegerField( 'Entry Type', choices=ENTRY_TYPE, default=1 )
    content = models.TextField( blank=True )
    sidebar = models.TextField( blank=True )

    images = models.ManyToManyField( Image, through='EntryRelationship', blank=True )
    order = models.PositiveIntegerField( 'Order',  default=1 )
    display = models.BooleanField( 'Is Displayed', default=1 )

    date = models.DateField( null=True, blank=True )
    
    def __unicode__( self ):
        return self.title

    def get_first_in_type( self ):
        try:
            e = Entry.objects.filter( entry_type=self.entry_type ).order_by('-order')[0]
            return e
        except IndexError:
            return false

    def get_last_in_type( self ):
        try:
            e = Entry.objects.filter( entry_type=self.entry_type ).order_by('order')[0]
            return e
        except IndexError:
            return false
    
    def get_list_display( self ):
        try:
            return self.images.get( entryrelationship__list_display=True ).src
        except Entry.DoesNotExist:
            return false

    def get_absolute_url(self):
        if self.entry_type == 0:
            root = 'typography'
        elif self.entry_type == 1:
            root = 'books'
        elif self.entry_type == 2:
            root = 'news'
        
        return 'thisiswrong'

        #return '/%s/%s/' %  ( root, self.order )

    
    def save(self, *args, **kwargs):
        e = self.get_first_in_type()
        if e and not self.pk:
            self.order = e.order + 1
            c = type(e).__name__
            if c == 'Typography':
                self.entry_type = 0
            elif c == 'Book':
                self.entry_type = 1
            elif c == 'News':
                self.entry_type = 2
        super(Entry, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ['-order']
        verbose_name_plural = 'Entries'


class Book ( Entry ):
    
    def get_absolute_url(self):
        return reverse('entries.views.book_detail'
                , kwargs = { 'order': self.order }
        )

    class Meta:
        verbose_name_plural = 'Books'
        proxy = True

class Typography ( Entry ):
    
    def get_absolute_url(self):
        return reverse('entries.views.typography_detail'
                , kwargs = { 'order': self.order }
        )

    class Meta:
        verbose_name_plural = 'Typography'
        proxy = True


class News ( Entry ):
    
    class Meta:
        verbose_name_plural = 'News'
        proxy = True

class EntryRelationship(models.Model):
    
    image = models.ForeignKey(Image)
    entry = models.ForeignKey(Entry)
    order = models.PositiveIntegerField( 'Order',  default=1, null=True, blank=True  )

    list_display = models.BooleanField( 'Front Image', default=0 )

    def __unicode__( self ):
        return 'Related Images'

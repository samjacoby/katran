from django.db import models
import os


class Image( models.Model ):

    def __unicode__( self ):
        return self.title

    title = models.CharField( max_length=100 )
    src = models.ImageField( upload_to='images' )

class Entry( models.Model ):

    images = models.ManyToManyField( Image, through='EntryRelationship', blank=True )
    order = models.PostiiveIntegerField( 'Order', blank=True, null=True )
    display = models.BooleanField( default=1 )

    class Meta:
        abstract = True
        ordering = ['-order']
        verbose_name_plural = 'Entries'

class Book ( Entry ):

    title = models.CharField( max_length=100 )
    subtitle = models.CharField( max_length=100, blank=True )
    content = models.TextField( blank=True )
    sidebar = models.TextField( blank=True )

    class Meta( Entry.Meta ):
        verbose_name_plural = 'Books'

class Typography ( Entry ):
    
    title = models.CharField( max_length=100 )
    subtitle = models.CharField( max_length=100, blank=True )
    content = models.TextField( blank=True )
    sidebar = models.TextField( blank=True )
    
    class Meta( Entry.Meta ):

class News ( Entry ):

    date = models.DateField( auto_now_add=True )
    content = models.TextField( blank=True )
    
    class Meta( Entry.Meta ):

class EntryRelationship(models.Model):
    
    image = models.ForeignKey(Image)
    entry = models.ForeignKey(Entry)
    cover = models.BooleanField( default=0 )

    def __unicode__( self ):
        return 'Related Images'


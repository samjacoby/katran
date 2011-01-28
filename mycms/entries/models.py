from django.db import models
import os


class Image( models.Model ):

    def __unicode__( self ):
        return self.title

    title = models.CharField( max_length=100 )
    src = models.ImageField( upload_to='images' )

class Entry( models.Model ):

    def __unicode__( self ):
        return self.title

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

    class Meta:
        ordering = ['-order']
        verbose_name_plural = 'Entries'

class Book ( Entry ):

    class Meta:
        verbose_name_plural = 'Books'
        proxy = True

class Typography ( Entry ):
    
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
    list_display = models.BooleanField( 'Front Image', default=0 )

    def __unicode__( self ):
        return 'Related Images'

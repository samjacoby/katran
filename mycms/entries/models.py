from django.db import models
import os



class Image( models.Model ):

    title = models.CharField( max_length=100 )
    src = models.ImageField( upload_to='images' )

class Entry( models.Model ):

    order = models.IntegerField( 'Order', blank=True, null=True )
    display = models.BooleanField( default=1 )

    class Meta:
        abstract = True

from django.db import models
from entries.models import Typography, Book, News
from cms.models import CMSPlugin

class BookPlugin( CMSPlugin ):
    book = models.ForeignKey('entries.Book', related_name='plugins')

    def __unicode__(self):
        return self.book.title


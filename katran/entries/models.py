from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from menus.menu_pool import menu_pool
from cms.models.fields import PlaceholderField


class EntryManager(models.Manager):

    def get_all_of_type(self, entry_type):
        return self.filter(entry_type=entry_type)

    def get_all_typography(self):
        return self.filter(entry_type=0)

    def get_all_books(self):
        return self.filter(entry_type=1)

class Entry(models.Model):

    objects = models.Manager()
    manager = EntryManager()

    title = models.CharField(max_length=100 , blank=True)
    subtitle = models.CharField(max_length=100, blank=True) 

    ENTRY_TYPE =(
           (0, 'Typography'),
           (1, 'Book'),
           )

    entry_type = models.IntegerField('Entry Type', choices=ENTRY_TYPE, default=1)

    cover = PlaceholderField('list_display_content', related_name='list_display')
    content = PlaceholderField('main_content')
    secondary_content = PlaceholderField('secondary_content', related_name='secondary_content')
    sidebar = PlaceholderField('sidebar_content', related_name='sidebar')

    order = models.PositiveIntegerField('Order',  default=1)
    display = models.BooleanField('Published', default=1)

    date = models.DateField(null=True, blank=True)
    
    def __unicode__(self):
        return self.title

    def get_first_in_type(self):
        try:
            e = Entry.objects.filter(entry_type=self.entry_type).order_by('-order')[0]
            return e
        except IndexError:
            return False

    def get_last_in_type(self):
        try:
            e = Entry.objects.filter(entry_type=self.entry_type).order_by('order')[0]
            return e
        except IndexError:
            return False
    
    def get_list_display(self):
        try:
            return self.images.get(entryrelationship__list_display=True).src
        except Entry.DoesNotExist:
            return False

    def get_absolute_url(self):
        if self.entry_type == 0:
            return reverse('entries.views.typography_detail' , kwargs = { 'order': self.order })
        elif self.entry_type == 1:
            return reverse('entries.views.book_detail' , kwargs = { 'order': self.order })
        
        return 'thisiswrong'

    
    def save(self, *args, **kwargs):

        # Invalidate the menu cache on creating/modifying objects
        menu_pool.clear(settings.SITE_ID, settings.LANGUAGE_CODE)
        
        if not self.pk:
            c = type(self).__name__
            if c == 'Typography':
                self.entry_type = 0
            elif c == 'Book':
                self.entry_type = 1

        e = self.get_first_in_type()

        # Auto-increment order
        if e and not self.pk:
            self.order = e.order + 1

        super(Entry, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ['-order']
        verbose_name_plural = 'Entries'


class Book(Entry):
    
    def get_absolute_url(self):
        return reverse('entries.views.book_detail', kwargs = { 'order': self.order })

    class Meta:
        verbose_name_plural = 'Books'
        proxy = True

class Typography(Entry):

    def get_absolute_url(self):
        return reverse('entries.views.typography_detail', kwargs = { 'order': self.order })

    class Meta:
        verbose_name_plural = 'Typography'
        proxy = True

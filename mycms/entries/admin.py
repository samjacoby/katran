from django.contrib import admin
import django.forms as forms
from entries.models import Image, Book, Typography, News, EntryRelationship

admin.site.register(Image)
admin.site.register(Book)
admin.site.register(Typography)
admin.site.register(News)

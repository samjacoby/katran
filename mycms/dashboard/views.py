# Create your views here.
import logging

from django.views.generic.simple import direct_to_template
from mycms.stamps import models

def index(request):

    context = {}

    items  = models.Designer.cobjects.list().select_related()
    context['items'] = items
    print items

    return direct_to_template(request, 'stamps/list.html', context)

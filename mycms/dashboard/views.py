# Create your views here.
import logging

from django.db.models import F
from django.http import HttpResponse
from django.views.generic.simple import direct_to_template
from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse


from mycms.stamps import models

log = logging.getLogger(__name__)

def index(request):

    context = {}

    items  = models.Designer.cobjects.list().select_related()
    context['items'] = items
    print items

    return direct_to_template(request, 'stamps/list.html', context)

def action(request):
    if not request.POST:
        log.error("Did not receive POST with this request; redirect")
        return redirect(reverse('dashboard_index')) 
    
    item_id = request.POST['id']
    order = int(request.POST['order']) + 1 # We use 1-indexing

    stamp = get_object_or_404(models.Stamp, pk=item_id)
    original_order = stamp.order

    
    if order < original_order:
        middle = models.Stamp.objects.filter(family=stamp.family, order__gte=order, order__lt=original_order)
        if middle is not None:
            middle.update(order=F('order') + 1)
        msg = "Updated ordering"
    elif order > original_order:
        middle = models.Stamp.objects.filter(family=stamp.family, order__gt=original_order, order__lte=order)
        if middle is not None:
            middle.update(order=F('order') - 1)
        msg = "Updated ordering"
    else:
        log.info("Order remains unchanged; redirect")
        msg = "Updated. Order unchanged"
         
    stamp.order = order
    stamp.save()

    return HttpResponse(msg)


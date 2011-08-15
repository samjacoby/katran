# Create your views here.
import logging

from django.db.models import F, Q
from django.http import HttpResponse
from django.views.generic.simple import direct_to_template
from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.forms.models import inlineformset_factory, modelformset_factory

import stamps.models

log = logging.getLogger(__name__)

@login_required
def index(request):

    context = {}

#    items  = stamps.models.Stamp.objects.ordered_list().select_related()
    #items  = stamps.models.Designer.cobjects.list().select_related()

    StampFormset = modelformset_factory(stamps.models.Stamp,form=stamps.models.StampForm, can_delete=True, max_num=0)
        
    if request.method == 'POST':
        formset = StampFormset(request.POST, request.FILES, queryset=stamps.models.Stamp.objects.ordered_list().select_related())
        if formset.is_valid():
            # do something with the formset.cleaned_data
            formset.save()
        else:
            print formset.errors
    else:
        formset = StampFormset(queryset=stamps.models.Stamp.objects.ordered_list().select_related())

    # Queryset is the list of objects, formset.forms, the corresponding forms
    # Zip together to allow iteration in one go in template
    formset.zipped = zip(formset.queryset, formset.forms)

    print formset.forms

    context['formset'] = formset

    return direct_to_template(request, 'dashboard/list.html', context)

@login_required
def action(request):

    if not request.POST:
        log.error("Did not receive POST with this request; redirect")
        return redirect(reverse('dashboard_index')) 
    
    action = request.POST['action']
    item_id = request.POST['id']
    order = int(request.POST['order']) + 1 # We use 1-indexing

    if action == 'family':
        model = stamps.models.Family
        obj = get_object_or_404(model, pk=item_id)
        Query = Q(designer=obj.designer) 
    elif action == 'stamp':
        model = stamps.models.Stamp
        obj = get_object_or_404(model, pk=item_id)
        Query = Q(family=obj.family) 
    else:
        log.error("Did not receive appropriate ACTION with this request; redirect")
        return redirect(reverse('dashboard_index'))

    original_order = obj.order

    if order < original_order:
        # Mass update ordering of other items
        middle = model.objects.filter(Query & Q(order__gte=order, order__lt=original_order))
        if middle is not None:
                middle.update(order=F('order') + 1)
        msg = "Updated ordering"
    elif order > original_order:
        middle = model.objects.filter(Query & Q(order__gt=original_order, order__lte=order))
        if middle is not None:
            middle.update(order=F('order') - 1)
        msg = "Updated ordering"
    else:
        log.info("Order remains unchanged")
         
    obj.order = order
    obj.save()

    return HttpResponse(msg)

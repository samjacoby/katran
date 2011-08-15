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
import dashboard.forms

log = logging.getLogger(__name__)

@login_required
def index(request):

    context = {}

    if request.method == 'POST':
   #     formset = dashboard.forms.DesignerFormset(request.POST, request.FILES)
#        family_formset = FamilyFormset(queryset=stamps.models.Family.objects.ordered_list().select_related(), prefix='family')
#        stamp_formset = StampFormset(queryset=stamps.models.Stamp.objects.ordered_list().select_related(), prefix='stamp')
        if formset.is_valid():
            pass
            # do something with the formset.cleaned_data
#            formset.save_all()
        else:
            print formset.errors
    else:
        #formset = dashboard.forms.DesignerFormset(queryset=stamps.models.Designer.cobjects.ordered_list())
        designers = stamps.models.Designer.objects.all()
        #formset = dashboard.forms.FamilyFormset(instance=designers[0])
        formset = dashboard.forms.DesignerFormset(queryset=designers)
#        formset = dashboard.forms.DesignerFormset()

    # Queryset is the list of objects, formset.forms, the corresponding forms
    # Zip together to allow iteration in one go in template
#    stamp_formset.zipped = zip(stamp_formset.queryset, stamp_formset.forms)
    context['designers'] = formset
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

    # Mass update ordering of other items
    if order < original_order:
        # If the new order is lower, select everything between the new order and the original order, and increment it one.
        middle = model.objects.filter(Query & Q(order__gte=order, order__lt=original_order))
        if middle is not None:
                middle.update(order=F('order') + 1)
        msg = "Updated ordering"
    elif order > original_order:
        # If the new order is greater, select everything greater and increment it one.
        middle = model.objects.filter(Query & Q(order__gt=original_order, order__lte=order))
        if middle is not None:
            middle.update(order=F('order') - 1)
        msg = "Updated ordering"
    else:
        log.info("Order remains unchanged")
         
    obj.order = order
    obj.save()

    return HttpResponse(msg)

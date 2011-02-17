# Main View
# Designer View
# Stamp Family/Stamp View

from stamps.models import Designer, Typeface, StampFamily, Stamp, Sponsor
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse                         
from django.template import RequestContext
from django.conf import settings
import os, re

def all_designers():
    '''
    Return ordered list of designers. Order by lower case last name.
    '''
    designer_list = Designer.objects.all().order_by('designer_class','last_name_id')
    return designer_list



def index(request):
    designer_list = all_designers()
    sponsor_list = Sponsor.objects.all()
    first_stamp_links = Stamp.get_stamp.first()
    return render_to_response('indices/index_stamps.html', { 'designer_list': designer_list
        , 'first_stamp': first_stamp_links
        , 'sponsor_list': sponsor_list }
        , context_instance=RequestContext(request))

def stamp(request, designer_name, stamp_family_id = 1, stamp_id = None):
    designer_list = all_designers()
    designer_name = designer_name.replace('_',' ')
    designer = Designer.objects.get(last_name_id__iexact=designer_name)
    stamp_list = Stamp.objects.filter(stamp_family__designer__last_name_id__iexact = designer_name, stamp_family__order = stamp_family_id)
    if not stamp_id:
        stamp = stamp_list[0]
    else:
        stamp = stamp_list.get(order = stamp_id)

    return render_to_response('stamps/detail_stamp.html'
            ,{'designer_list':designer_list,'designer':designer,'stamp':stamp}
            ,context_instance=RequestContext(request))


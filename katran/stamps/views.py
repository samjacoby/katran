from django.db.models import F, Q
from stamps.models import Designer, Family, Stamp, Sponsor
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse


def index(request):
    
    context = {}

    designers = Designer.cobjects.list()
    sponsors = Sponsor.objects.filter(active=True)

    context['sponsors'] = sponsors
    context['designers'] = designers

    return render_to_response('stamps/index.html',
                              context,
                              context_instance=RequestContext(request))

def detail(request, designer, family=1, stamp=1, url_override=''):

    if url_override:
        Query = Q(url_override=url_override)
    else:
        Query = Q(order=stamp)

    stamp = Stamp.objects.filter(Q(family__designer__normalized_name__iexact=designer, family__order=family) & Query)[0] 

    return render_to_response('stamps/detail.html',
                             {'stamp': stamp },
                              context_instance=RequestContext(request))

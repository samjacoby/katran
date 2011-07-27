from stamps.models import Designer, Family, Stamp, Sponsor
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse


def index(request):
    return render_to_response('stamps/index.html',
                              context_instance=RequestContext(request))

def detail(request, designer, family=1, stamp=1, url_override=''):

    stamp = get_object_or_404(Stamp, family__designer__normalized_name__iexact=designer,
                                     family__order=family, 
                                     order=stamp,
                                     url_override=url_override)
    
    return render_to_response('stamps/detail.html',
                             {'stamp': stamp },
                              context_instance=RequestContext(request))


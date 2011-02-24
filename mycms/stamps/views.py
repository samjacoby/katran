from stamps.models import Designer, Family, Stamp, Sponsor
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext


def index(request):
    return 'what'

def detail(request, designer, family = 1, stamp = 1):

    stamp = get_object_or_404( 
        Stamp
        , family__designer__normalized_name__iexact = designer
        , family__order = family
        , order = stamp )
    
    return render_to_response('stamps/detail.html'
                                , { 'stamp': stamp }
                                , context_instance = RequestContext(request))



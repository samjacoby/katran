from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from entries.models import Entry

def fetch_object( entry_type, order ):
    e = Entry.manager.get_all_of_type( entry_type ).get( order=order )
    return e

def book_detail( request, entry_type, order ):
    e = fetch_object( entry_type, order)
    return render_to_response('entries/book_detail.html', {'e': e, }, context_instance=RequestContext(request))

def typography_detail(request, entry_type, order ):
    e = fetch_object( entry_type, order)
    return render_to_response('entries/typography_detail.html', {'e': e, }, context_instance=RequestContext(request))

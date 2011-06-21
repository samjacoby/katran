#!/usr/bin/env python
from lxml.html import soupparser
from lxml.etree import tostring
from lxml.cssselect import CSSSelector
from optparse import OptionParser
import re, os, csv
from django.core.management.base import NoArgsCommand
from katran.stamps.models import Designer, StampFamily, Stamp, Sponsor, Typeface, Footer

class Command(NoArgsCommand):

    help = "Import Settings"

#    option_list = NoArgsCommand.option_list + (
#        make_option('--verbose', action='store_true'),
#    )

    def handle_noargs(self, **options):
        StampFileIter()

def StampFileIter():           
    path = '/home/sjacoby/job/katran/html_stamps'
    file_list = os.listdir(path)
    for file_name in file_list:
        print file_name
        file_path = os.path.join(path, file_name)
        stamp = StampParse(file_path)
        if stamp:
            CreateStamp(stamp)

def CreateStamp(stamp):                                                                
    last_name_id = stamp['designer_last_name'].lower().replace(' ','')
    d, created = Designer.objects.get_or_create(last_name = stamp['designer_last_name'],
            last_name_id = last_name_id)
    d.save()
    s_f, created = StampFamily.objects.get_or_create(designer = d, name='', order = stamp['stamp_family'])
    s_f.save()

    s = Stamp(stamp_family = s_f, name='', img = stamp['src'], order = stamp['stamp_id'])
    s.save()

def StampParse(file_name):
    f = open(file_name)
    r = soupparser.parse(f)
    (head, tail) = os.path.split(file_name)
    pattern = r'stamps_(?P<designer>[a-z]+)\D+(?P<stamp_family>\d+)\D+(?P<stamp_id>\d+)\D+'
    m = re.match(pattern, tail)
    if m:
        designer = m.group('designer')
        stamp_family = m.group('stamp_family')
        stamp_id = m.group('stamp_id')
    else:            
        print "no match"
        return None

    img_sel = CSSSelector('a img')
    for el in img_sel(r.getroot()):
        src = el.get('src')
    
    #print '%s,%s,%s,%s' % (designer, stamp_family, stamp_id, src)
    return {'designer_last_name':designer.capitalize(), 'stamp_family':stamp_family, 'stamp_id':stamp_id, 'src':src}

if __name__ == '__main__':    
    
    StampFileIter()


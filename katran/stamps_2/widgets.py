import django.forms as forms
import os
from string import Template
from django.conf import settings
from django.utils.encoding import StrAndUnicode, force_unicode
from django.forms.util import flatatt
from django.utils.safestring import mark_safe

class AdminImageWidget(forms.TextInput):
  def render(self, name, value, attrs=None):
    output = []
    if value:
        path = os.path.join(settings.STATIC_URL, value)
        output.append('<img style="float:right" src="%s"></img>' % path)
    output.append(super(forms.TextInput, self).render(name, value, attrs))
    return mark_safe(u''.join(output))


'''
 def render(self, name, value, attrs=None):
        output = []
        file_name = str(value)
        if file_name:
            file_path = '%s%s' % (settings.MEDIA_URL, file_name)
            try:            # is image
                Image.open(os.path.join(settings.MEDIA_ROOT, file_name))
                output.append('<a target="_blank" href="%s">%s</a><br />%s <a target="_blank" href="%s">%s</a><br />%s ' % \
                    (file_path, thumbnail(file_name), _('Currently:'), file_path, file_name, _('Change:')))
            except IOError: # not image
                output.append('%s <a target="_blank" href="%s">%s</a> <br />%s ' % \
                    (_('Currently:'), file_path, file_name, _('Change:')))
            
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))
'''

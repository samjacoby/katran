from django.forms.models import ModelForm
from django.utils.translation import ugettext_lazy as _
from django import forms

from stamps.models import Stamp
from stamps.plugins.stamplink.models import StampLink

class StampLinkForm(ModelForm):
    page_link = forms.ModelChoiceField(label=_("page"), queryset=Stamp.objects.ordered_list(), required=False)
    
    def for_site(self, site):    
        # override the page_link fields queryset to contain just pages for
        # current site
        self.fields['page_link'].queryset = Stamp.objects.ordered_list()
    
    class Meta:
        model = StampLink
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')

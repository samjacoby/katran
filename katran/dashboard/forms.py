from django import forms
from django.forms.models import BaseFormSet, BaseModelFormSet, BaseInlineFormSet
from django.forms import ModelForm
from django.forms.models import inlineformset_factory, modelformset_factory
from django.forms.formsets import DELETION_FIELD_NAME

import stamps.models
import dashboard.forms

class BaseDesignerFormset(BaseModelFormSet):

    def is_valid(self):
        result = super(BaseDesignerFormset, self).is_valid()
 
        for form in self.forms:
            if hasattr(form, 'nested'):
                for n in form.nested:
                    # make sure each nested formset is valid as well
                    result = result and n.is_valid()
 
        return result

#    def save_new(self, form, commit=True):
#        """Saves and returns a new model instance for the given form."""
#
#        instance = super(BaseDesignerFormset, self).save_new(form, commit=commit)
#        # update the form's instance reference
#        form.instance = instance
#
#        # update the instance reference on nested forms
#        for nested in form.nested:
#            nested.instance = instance
#
#            # iterate over the cleaned_data of the nested formset and update the foreignkey reference
#            for cd in nested.cleaned_data:
#                cd[nested.fk.name] = instance
#
#        return instance
#
#    def save_all(self, commit=True):
#        """Save all formsets and along with their nested formsets."""
#
#        # Save without committing (so self.saved_forms is populated)
#        # -- We need self.saved_forms so we can go back and access
#        #    the nested formsets
#        objects = self.save(commit=False)
#
#        # Save each instance if commit=True
#        if commit:
#            for o in objects:
#                o.save()
#
#        # save many to many fields if needed
#        if not commit:
#            self.save_m2m()
#
#        # save the nested formsets
#        for form in set(self.initial_forms + self.saved_forms):
#            if self.should_delete(form): continue
#
#            for nested in form.nested:
#                nested.save(commit=commit)
class BaseFamilyFormset(BaseInlineFormSet): 

    def __init__(self, *args, **kwargs): 
        # Initialize empty next to avoid overwriting with subsequent families
        self.nested = []
        super(BaseFamilyFormset, self).__init__(*args, **kwargs)

    def is_valid(self):
        result = super(BaseFamilyFormset, self).is_valid()
 
        for form in self.forms:
            if hasattr(form, 'nested'):
                for n in form.nested:
                    # make sure each nested formset is valid as well
                    result = result and n.is_valid()
 
        return result

    def add_fields(self, form, index):
        # allow the super class to create the fields as usual
        super(BaseFamilyFormset, self).add_fields(form, index)

        # created the nested formset
        try:
            instance = self.get_queryset()[index]
            pk_value = instance.pk
        except IndexError:
            instance=None
            pk_value = hash(form.prefix)

        # Make sure data is 'None', not just empty, as this counts as bound in django
        if not self.data:
            self.data = None

        # store the formset in the .nested property
        self.nested.extend([StampFormset(data=self.data, instance=instance, prefix='STAMP_%s' % pk_value)])

    def save_new(self, form, commit=True):
        """Saves and returns a new model instance for the given form."""

        instance = super(BaseFamilyFormset, self).save_new(form, commit=commit)
        # update the form's instance reference
        form.instance = instance

        # update the instance reference on nested forms
        for nested in self.nested:
            nested.instance = instance

            # iterate over the cleaned_data of the nested formset and update the foreignkey reference
            for cd in nested.cleaned_data:
                cd[nested.fk.name] = instance

        return instance

    def should_delete(self, form):
          """Convenience method for determining if the form's object will
          be deleted; cribbed from BaseModelFormSet.save_existing_objects."""
   
          if self.can_delete:
              raw_delete_value = form._raw_value(DELETION_FIELD_NAME)
              should_delete = form.fields[DELETION_FIELD_NAME].clean(raw_delete_value)
              return should_delete
   
          return False

    def save_all(self, commit=True):
        """Save all formsets and along with their nested formsets."""

        # Save without committing (so self.saved_forms is populated)
        # -- We need self.saved_forms so we can go back and access
        #    the nested formsets
        objects = self.save(commit=False)

        # Save each instance if commit=True
        if commit:
            for o in objects:
                o.save()

        # save many to many fields if needed
        if not commit:
            self.save_m2m()

        # save the nested formsets
        for form in set(self.initial_forms + self.saved_forms):
            if self.should_delete(form): continue

            for nested in self.nested:
                nested.save(commit=commit)

class BaseStampFormset(BaseInlineFormSet):
     def add_fields(self, form, index):
         super(BaseStampFormset, self).add_fields(form, index)
         #form.fields["my_field"] = forms.CharField()
         print index

class DesignerForm(ModelForm):

    class Meta:
        model = stamps.models.Designer
        exclude = ('order','info')

class StampForm(ModelForm):

    class Meta:
        model = stamps.models.Stamp
        exclude = ('order','footer','info')

DesignerFormset = modelformset_factory(stamps.models.Designer, exclude=('info','order'), formset=BaseDesignerFormset, extra=0)
FamilyFormset = inlineformset_factory(stamps.models.Designer, stamps.models.Family, exclude=('order',), formset=BaseFamilyFormset, extra=0)
StampFormset = inlineformset_factory(stamps.models.Family, stamps.models.Stamp, formset=BaseStampFormset, exclude=('footer', 'info', 'order'), extra=0)

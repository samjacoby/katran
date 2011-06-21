from django.contrib import admin
from django.contrib.contenttypes import generic
from stamps.models import Designer, StampFamily, Stamp, Sponsor, Typeface, Footer
from widgets import AdminImageWidget
from django.forms import ModelForm, Textarea

class SponsorInline(generic.GenericStackedInline):
    model = Sponsor
    extra = 0

class FooterInline(generic.GenericStackedInline):
    model = Footer
    extra = 0

class StampInlineForm(ModelForm):
    class Meta:
        model = Stamp
        widgets = {
                'img': AdminImageWidget(attrs={'class':'vTextField', 'type':"text", 'id':'id_img'}) 
        }

    
class StampInline(admin.StackedInline):
    form = StampInlineForm
    model = Stamp
    extra = 0

class StampFamilyInline(admin.StackedInline):
    model = StampFamily
    extra = 0

class TypefaceInline(admin.StackedInline):
    model = Typeface
    extra = 0

class StampFamilyAdmin(admin.ModelAdmin):
    fieldsets = (
            (None, {
                'fields':('designer', 'name', ('country', 'year'),'order'),
                'description':('One stamp family, many stamps.')
                }),
            )
    list_display = ('designer', 'name', 'order')
    list_editable = ['name']
    ordering = ('designer__last_name_id', 'order')
    inlines = [ 
            StampInline,
            FooterInline,
            SponsorInline,
            ]

class StampForm(ModelForm):
    class Meta:
        model = Stamp
        widgets = {  
            'img': AdminImageWidget(attrs={'class':'vTextField', 'type':"text", 'id':'id_img'})
        }

class StampAdmin(admin.ModelAdmin):
    inlines = [ 
            FooterInline,
            SponsorInline,
        ]
    fields = ['stamp_family', 'name', 'value', 'img', 'order']
    form = StampForm
    list_display = ('stamp_family','name', 'admin_image', 'value','order')
    list_display_links = ['stamp_family']
    list_editable = ['name','value']
    search_fields = ['stamp_family__name','stamp_family__designer__last_name','name']
    ordering = ('stamp_family__designer__last_name_id', 'order')

class DesignerAdmin(admin.ModelAdmin):
    list_display = ('last_name','first_name')
    list_editable = ('first_name',)
    exclude = ('last_name_id',)             
    ordering = ('last_name_id',)
    inlines = [
            TypefaceInline,
            StampFamilyInline,
            FooterInline,
            SponsorInline,
            ]

admin.site.register(Designer, DesignerAdmin)
admin.site.register(StampFamily, StampFamilyAdmin)
admin.site.register(Stamp, StampAdmin)
admin.site.register(Sponsor)

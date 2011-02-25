from django.contrib import admin
from cms.admin.placeholderadmin import PlaceholderAdmin
from stamps.models import Designer, Family, Stamp, Sponsor

class FamilyInline(admin.StackedInline):
    model = Family
    extra = 0

class StampInline(admin.StackedInline):
    model = Stamp
    extra = 0

class DesignerAdmin(PlaceholderAdmin):
   list_display = ('display_name',)
   inlines = [FamilyInline]
   class Media:
        js = ('js/stamp-utils.js',)

class FamilyAdmin(PlaceholderAdmin):
    list_display = ('designer', 'name', 'order')
    inlines = [StampInline]
    #list_editable = ['order']

class StampAdmin(PlaceholderAdmin):
    list_display = ('family', 'name', 'order')
    #list_editable = ['order']

admin.site.register(Designer, DesignerAdmin)
admin.site.register(Family, FamilyAdmin)
admin.site.register(Stamp, StampAdmin)

from django.contrib import admin
from cms.admin.placeholderadmin import PlaceholderAdmin
from django.contrib.contenttypes import generic
from stamps.models import Designer, Family, Stamp, Sponsor

#class SponsorInline(generic.GenericStackedInline):
class SponsorInline(admin.StackedInline):
    model = Sponsor
    extra = 0

class FamilyInline(admin.StackedInline):
    model = Family
    extra = 0
    fieldsets = (
        (None, {
            'fields': ['name', ('is_published', 'in_navigation')]
        }),
        )

class StampInline(admin.StackedInline):
    model = Stamp
    exclude = ('info', 'footer')
    extra = 0

class DesignerAdmin(PlaceholderAdmin):
   list_display = ('name',)
   exclude = ('info',)
   class Media:
        js = ('js/stamp-utils.js',)

class FamilyAdmin(PlaceholderAdmin):
    list_display = ('designer', 'name', 'order')
    inlines = [StampInline]

class StampAdmin(PlaceholderAdmin):
    list_display = ('family', 'name', 'order')

admin.site.register(Designer, DesignerAdmin)
admin.site.register(Family, FamilyAdmin)
admin.site.register(Stamp, StampAdmin)
admin.site.register(Sponsor)

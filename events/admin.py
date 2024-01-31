from django.contrib import admin
#from .models import Event,Blog, Dashboard, Organizer, CurrentEvent
from .models import Event, Blog

class EventAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('category_type',)  

    def get_queryset(self, request):
        return super().get_queryset(request).filter(category_type='E')

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('category',)  


admin.site.register(Event, EventAdmin)
admin.site.register(Blog, BlogAdmin)



#admin.site.register(Event)
#admin.site.register(Blog)
#admin.site.register(Dashboard)
#admin.site.register(Organizer)
#admin.site.register(CurrentEvent)
admin.site.site_header = " LIVE IN NAIROBI"
admin.site.site_title = 'LiveInNBO'
admin.site.index_title = 'Admin Dashboard'
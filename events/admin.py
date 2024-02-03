from django.contrib import admin
#from .models import Event,Blog, Dashboard, Organizer, CurrentEvent
from .models import Event, Blog

 

admin.site.register(Event)
admin.site.register(Blog)
#admin.site.register(Dashboard)
#admin.site.register(Organizer)
#admin.site.register(CurrentEvent)
admin.site.site_header = " LIVE IN NAIROBI"
admin.site.site_title = 'LiveInNBO'
admin.site.index_title = 'Admin Dashboard'
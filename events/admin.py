from django.contrib import admin
from .models import Event, Blog, CartItem, Profile

 

admin.site.register(Event)
admin.site.register(Blog)
admin.site.register(CartItem)
admin.site.register(Profile)


admin.site.site_header = " LIVE IN NAIROBI"
admin.site.site_title = 'LiveInNBO'
admin.site.index_title = 'Admin Dashboard'
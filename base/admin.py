from django.contrib import admin
from .models import Service, User, Offer, Messages

admin.site.register(Service)
admin.site.register(User)
admin.site.register(Offer)
admin.site.register(Messages)


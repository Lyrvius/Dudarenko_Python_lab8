from django.contrib import admin

# Register your models here.

from .models import Client, Car, Repair

admin.site.register(Client)
admin.site.register(Car)
admin.site.register(Repair)

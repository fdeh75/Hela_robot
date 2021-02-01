from django.contrib import admin

# Register your models here.

from .models import City, Job_type, Job_ad

admin.site.register(City)
admin.site.register(Job_type)
admin.site.register(Job_ad)
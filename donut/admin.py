from django.contrib.gis import admin

from donut.models import Shop

admin.site.register(Shop, admin.ModelAdmin)

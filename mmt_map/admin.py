# Django core
from django.contrib.gis import admin

# Memory Map Toolkit
from .models import Theme, Point, Polygon, Document


# 3rd Party

# Register your models here.

admin.site.register(Theme)
admin.site.register(Document)
admin.site.register(Point, admin.GeoModelAdmin)
admin.site.register(Polygon, admin.GeoModelAdmin)
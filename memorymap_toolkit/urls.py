"""memorymap_toolkit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from mmt_map.models import Point, Polygon, Line
from mmt_pages.models import Page

point_dict = {
    'queryset': Point.objects.filter(published=True)
}

line_dict = {
    'queryset': Line.objects.filter(published=True)
}

polygon_dict = {
    'queryset': Polygon.objects.filter(published=True)
}

admin.site.site_header = "Memory Map Toolkit Admin"
admin.site.site_title = "Memory Map Toolkit Admin"
admin.site.index_title = "Welcome to the Memory Map Toolkit"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mmt_map.urls')),
    path('api/', include('mmt_api.urls')),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('sitemap.xml', sitemap, 
        {
            'sitemaps': 
                {
                    'points': GenericSitemap(point_dict, priority=0.6),
                    'polygons': GenericSitemap(polygon_dict, priority=0.6),
                    'lines': GenericSitemap(line_dict, priority=0.6),
                }
        }, 
        name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
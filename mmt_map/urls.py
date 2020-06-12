# Django core
from django.urls import path, re_path

# 3rd Party Modules

# Memory Map Toolkit
from . import views
from .models import Point

urlpatterns = [
	path('', views.index, name='index'),
	path('features/detail/<str:source_layer>/<int:pk>', views.feature_detail, name='feature_detail'),
	re_path(r'tiles/(?P<z>\d+)/(?P<x>\d+)/(?P<y>\d+)\.(?P<tile_format>\w+)$', views.vector_tile, name='vector_tile'),
    re_path(r'tiles/interactive\.json', views.tile_json, name='tile_json'),
]
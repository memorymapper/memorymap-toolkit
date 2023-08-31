# Django core
from django.urls import path, re_path

# 3rd Party Modules

# Memory Map Toolkit
from . import views

urlpatterns = [
	# V1.0 urls
	path('1.0/features/', views.feature_list, name='feature_list'),
	path('1.0/features/<str:source_layer>/<int:pk>', views.feature, name='feature'),
	path('1.0/features/search/', views.search_features, name='search_features'),
	path('1.0/features/theme/', views.get_features_by_theme, name='get_features_by_theme'),
	path('1.0/features/tag/', views.get_features_by_tag, name='get_features_by_tag'),
    path('1.0/features/attachments/documents/<int:pk>', views.document, name='document'),
    path('1.0/features/<str:source_layer>/<int:pk>/attachments/', views.feature_attachments, name='attachments'),
    path('1.0/pages/<str:slug>', views.page, name='page'),
    path('1.0/pages/', views.pages, name='pages'),
	# V2.0 urls
	path('2.0/config/', views.site_config, name='site_config'),
	path('2.0/themes/', views.theme_list, name='theme_list'),
	path('2.0/features/<uuid:uuid>', views.feature_by_uuid, name='feature_by_uuid'),
	path('2.0/features/<uuid:uuid>/detail', views.feature_detail_by_uuid, name='feature_detail_by_uuid'),
	path('2.0/features/attachments/documents/', views.DocumentList.as_view(), name='document_list'),
	path('2.0/features/<uuid:uuid>/attachments', views.feature_attachments_by_uuid, name='attachments_by_uuid'),
	path('2.0/features/<uuid:uuid>/attachments/<slug:slug>', views.feature_document_by_uuid, name='documents_by_uuid'),
	path('2.0/search/', views.search, name='search'),
	path('2.0/pages/front/', views.front_page, name='front_page'),
]



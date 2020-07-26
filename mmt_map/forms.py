from django.contrib.gis import forms
from .models import Point, Polygon, Line
from .widgets import MapBoxGLWidget
from constance import config

class PointForm(forms.ModelForm):
	class Meta:
		model = Point
		fields = ['name', 'geom', 'theme', 'banner_image', 'banner_image_copyright', 'popup_image', 'popup_audio_title', 'popup_audio_slug', 'popup_audio_file', 'weight', 'tags', 'published',]

	geom = forms.PointField(widget=MapBoxGLWidget(attrs={'config': config}))


class PolygonForm(forms.ModelForm):
	class Meta:
		model = Polygon
		fields = ['name', 'geom', 'theme', 'banner_image', 'banner_image_copyright', 'popup_image', 'popup_audio_title', 'popup_audio_slug', 'popup_audio_file', 'weight', 'tags', 'published',]

	geom = forms.MultiPolygonField(widget=MapBoxGLWidget(attrs={'config': config}))


class LineForm(forms.ModelForm):
	class Meta:
		model = Line
		fields = ['name', 'geom', 'theme', 'banner_image', 'banner_image_copyright', 'popup_image', 'popup_audio_title', 'popup_audio_slug', 'popup_audio_file', 'weight','tags', 'published',]

	geom = forms.MultiLineStringField(widget=MapBoxGLWidget(attrs={'config': config}))
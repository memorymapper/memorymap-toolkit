from django.contrib.gis import forms
from django.utils.translation import gettext_lazy as _
from .models import Point, Polygon, Line, MultiPoint
from .widgets import MapBoxGLWidget
from constance import config


class PointForm(forms.ModelForm):
	class Meta:
		model = Point
		
		fields = ['name', 'geom', 'description', 'theme', 'popup_image', 'popup_audio_file', 'popup_audio_title', 'popup_audio_slug', 'banner_image', 'banner_image_copyright', 'weight', 'tags', 'published',]

		help_texts = {
			'popup_audio_title': _('If you have added an audio file to the popup, make sure you give it a title as well'),
			'description': _('A short description of the location.')
		}

	geom = forms.PointField(widget=MapBoxGLWidget(attrs={'config': config}), label=_('Point'))


class MultiPointForm(forms.ModelForm):
	class Meta:
		model = MultiPoint
		
		fields = ['name', 'geom', 'description', 'theme', 'popup_image', 'popup_audio_file', 'popup_audio_title', 'popup_audio_slug', 'banner_image', 'banner_image_copyright', 'weight', 'tags', 'published',]

		help_texts = {
			'popup_audio_title': _('If you have added an audio file to the popup, make sure you give it a title as well'),
			'description': _('A short description of the location.')
		}

	geom = forms.MultiPointField(widget=MapBoxGLWidget(attrs={'config': config}), label=_('Points'))




class PolygonForm(forms.ModelForm):
	class Meta:
		model = Polygon
		
		fields = ['name', 'geom', 'description', 'theme', 'popup_image', 'popup_audio_file', 'popup_audio_title', 'popup_audio_slug', 'banner_image', 'banner_image_copyright', 'weight', 'tags', 'published',]

		help_texts = {
			'popup_audio_title': _('If you have added an audio file to the popup, make sure you give it a title as well'),
			'description': _('A short description of the location.')
		}

	geom = forms.MultiPolygonField(widget=MapBoxGLWidget(attrs={'config': config}), label=_('Polygon'))


class LineForm(forms.ModelForm):
	class Meta:
		model = Line

		fields = ['name', 'geom', 'description', 'theme', 'popup_image', 'popup_audio_file', 'popup_audio_title', 'popup_audio_slug', 'banner_image', 'banner_image_copyright', 'weight', 'tags', 'published',]

		help_texts = {
			'popup_audio_title': _('If you have added an audio file to the popup, make sure you give it a title as well'),
			'description': _('A short description of the location.')
		}

	geom = forms.MultiLineStringField(widget=MapBoxGLWidget(attrs={'config': config}), label=_('Line'))
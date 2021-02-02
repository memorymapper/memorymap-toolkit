# Django core
from django.contrib.gis import forms

# Third Party Django apps
from constance import config

class MapBoxGLWidget(forms.BaseGeometryWidget):
	template_name = 'mmt_map/forms/widgets/mapboxgl_widget.html'

	# Return the geometry as geojson so it plays nice with MapBoxGL

	def serialize(self, value):
		return value.json if value else ''

	class Media:
		css = {
			'all': ('https://api.tiles.mapbox.com/mapbox-gl-js/' + config.MAPBOX_VERSION + '/mapbox-gl.css', 'https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-draw/v1.2.0/mapbox-gl-draw.css')
		}
		js = ('https://api.tiles.mapbox.com/mapbox-gl-js/' + config.MAPBOX_VERSION + '/mapbox-gl.js', 'https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-draw/v1.2.0/mapbox-gl-draw.js', 'https://cdn.jsdelivr.net/npm/@turf/turf@5/turf.min.js')
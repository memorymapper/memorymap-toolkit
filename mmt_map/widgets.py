from django.contrib.gis import forms

class MapBoxGLWidget(forms.BaseGeometryWidget):
	template_name = 'mmt_map/forms/widgets/mapboxgl_widget.html'

	# Return the geometry as geojson so it plays nice with MapBoxGL

	def serialize(self, value):
		return value.json if value else ''

	class Media:
		css = {
			'all': ('https://api.tiles.mapbox.com/mapbox-gl-js/v1.6.1/mapbox-gl.css', 'https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-draw/v1.0.9/mapbox-gl-draw.css')
		}
		js= ('https://api.tiles.mapbox.com/mapbox-gl-js/v1.6.1/mapbox-gl.js', 'https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-draw/v1.0.9/mapbox-gl-draw.js', 'https://cdn.jsdelivr.net/npm/@turf/turf@5/turf.min.js')
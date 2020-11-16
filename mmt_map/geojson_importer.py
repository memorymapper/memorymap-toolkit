from django.contrib.gis.geos import GEOSGeometry

from .models import Point, Polygon, Line, Theme

import json

class GeoJsonImporter():
	def __init__(self, file, theme=None, name_field=None, published=True):
		"""
		Utility class for importing GeoJson FeatureCollections		

		param str file - path to geojson file object
		param str theme = optional parameter to add all imported features to a theme
		param str name_field = optional parameter to populate the 'name' of each feature from the geojson feature properties. If no value is given features will be given a numeric value as a name.
		param bool published = by default, all imported features will be published on the map. Set this to 'False' to override this behaviour.
		"""

		with open(file) as f:
			self.geojson = json.load(f)

		if theme != None:
			t = Theme.objects.get_or_create(name=theme)
			self.theme = t
		else:
			self.theme = None

		if name_field != None:
			self.name_field = name_field
		else:
			self.name_field = None

		self.published = published

	def save_feature_collection(self):
		count = 0
		for f in self.geojson['features']:
			feature = None

			if self.name_field != None:
				name = f['properties'][self.name_field]
			else:
				name = str(count)

			geom = GEOSGeometry(json.dumps(f['geometry']))

			if f['geometry']['type'] == 'Point':
				feature = Point.objects.get_or_create(name=name, geom=geom, published=self.published)
			elif f['geometry']['type'] == 'Polygon':
				feature = Polygon.objects.get_or_create(name=name, geom=geom, published=self.published)
			elif f['geometry']['type'] == 'LineString':
				feature = Line.objects.get_or_create(name=name, geom=geom, published=self.published)
			
			if self.theme is not None:
				feature[0].theme = self.theme[0]
				feature[0].save()

			count += 1



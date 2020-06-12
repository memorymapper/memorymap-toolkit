# Django Core
from django.test import TestCase
from django.contrib.gis.geos import Point, LineString, MultiLineString, Polygon, MultiPolygon

# Memory Map Toolkit
from .models import Theme, AbstractFeature
from .models import Point as MmtPoint
from .models import Line as MmtLine
from .models import Polygon as MmtPolygon

# Model Tests

class ThemeModelTestCase(TestCase):
	"""Theme tests"""
	
	def create_theme(self):
		return Theme.objects.create(name='test theme')

	def test_theme_creation(self):
		"""Make sure a theme is created properly"""

		theme = self.create_theme()
		self.assertTrue(isinstance(theme, Theme))
		self.assertEqual(theme.__str__(), theme.name)


class AbstractFeatureModelTestCase(TestCase):
	"""Abstract Feature tests"""
	
	def create_point(self):
		point = Point(0,0)
		return MmtPoint.objects.create(name='test point', geom=point)

	def create_line(self):
		line_1 = LineString((0,0), (1,1))
		line_2 = LineString((1,1), (2,2))
		multiline = MultiLineString(line_1, line_2)
		return MmtLine.objects.create(name='test line', geom=multiline)

	def create_polygon(self):
		poly_1 = Polygon(((0, 0), (0, 1), (1, 1), (0, 0)))
		poly_2 = Polygon(((1, 1), (1, 2), (2, 2), (1, 1)))
		multipoly = MultiPolygon(poly_1, poly_2)
		return MmtPolygon.objects.create(name='test polygon', geom=multipoly)

	def test_feature_creation(self):
		# Create a feature of the correct type depending on which child model is being tested
		feature = None
		if (isinstance(self, PointModelTestCase)):
			feature = self.create_point()
		elif (isinstance(self, LineModelTestCase)):
			feature = self.create_line()
		elif (isinstance(self, PolygonModelTestCase)):
			feature = self.create_polygon()

		## Dont run the test on the actual abstract model
		if feature is not None:
			# Check the url returns correctly
			geom_type = feature.__class__.__name__.lower()
			correct_url = '/?feature_type=' + geom_type + '&id=' + str(feature.id)
			self.assertEqual(feature.get_absolute_url(), correct_url)

			# Check that the __str__ method returns correctly
			self.assertEqual(feature.__str__(), feature.name)


class PointModelTestCase(AbstractFeatureModelTestCase):
	"""Point tests"""


class LineModelTestCase(AbstractFeatureModelTestCase):
	"""Line tests"""



class PolygonModelTestCase(AbstractFeatureModelTestCase):
	"""Polygon tests"""

		
# View Tests
# Django Core
from django.test import TestCase
from django.contrib.gis.geos import Point, LineString, MultiLineString, Polygon, MultiPolygon
from django.core.files.uploadedfile import SimpleUploadedFile

# Third party Django apps
from easy_thumbnails.files import get_thumbnailer
from filer.models import File

# Memory Map Toolkit
from .models import Theme, AbstractFeature, AbstractAttachment, Document, Image, AudioFile, feature_directory_path
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
	"""Feature tests. Covers all feature types - points, lines, polygons - despite the 'Abstract' prefix. Called Abstract as Point, Line, and Polygon models all inherit from the AbstractFeature class in models.py."""

	test_img = SimpleUploadedFile(name='Walter_Benjamin.jpg', content=open('mmt_map/Walter_Benjamin.jpg', 'rb').read(), content_type='image/jpeg')

	test_audio_file = SimpleUploadedFile(name='Songs_of_innocence_and_experience_the_ecchoing_green_blake.mp3', content=open('mmt_map/Songs_of_innocence_and_experience_the_ecchoing_green_blake.mp3', 'rb').read(), content_type='audio/mpeg')
	
	def create_point(self):
		point = Point(0,0)
		return MmtPoint(name='test point', geom=point, popup_image=self.test_img, banner_image=self.test_img, popup_audio_file=File(file=self.test_audio_file).save())

	def create_line(self):
		line_1 = LineString((0,0), (1,1))
		line_2 = LineString((1,1), (2,2))
		multiline = MultiLineString(line_1, line_2)
		return MmtLine(name='test line', geom=multiline, popup_image=self.test_img, banner_image=self.test_img, popup_audio_file=File(file=self.test_audio_file).save())

	def create_polygon(self):
		poly_1 = Polygon(((0, 0), (0, 1), (1, 1), (0, 0)))
		poly_2 = Polygon(((1, 1), (1, 2), (2, 2), (1, 1)))
		multipoly = MultiPolygon(poly_1, poly_2)
		return MmtPolygon(name='test polygon', geom=multipoly, popup_image=self.test_img, banner_image=self.test_img, popup_audio_file=File(file=self.test_audio_file).save())

	def test_feature_creation(self):
		# Create a feature of the correct type depending on which child model is being tested
		feature = None
		if (isinstance(self, PointModelTestCase)):
			feature = self.create_point()
			feature.save()
		elif (isinstance(self, LineModelTestCase)):
			feature = self.create_line()
			feature.save()
		elif (isinstance(self, PolygonModelTestCase)):
			feature = self.create_polygon()
			feature.save()


		## Dont run the test on the actual abstract model
		if feature is not None:
			# Check the url returns correctly
			geom_type = feature.__class__.__name__.lower()
			correct_url = '/?feature_type=' + geom_type + '&id=' + str(feature.id)
			self.assertEqual(feature.get_absolute_url(), correct_url)

			# Check that the __str__ method returns correctly
			self.assertEqual(feature.__str__(), feature.name)

			# Check that the get_*_url methods work
			if feature.popup_image:
				correct_popup_image_url = get_thumbnailer(feature.popup_image)['site_small'].url
				self.assertEqual(feature.get_popup_image_url(), correct_popup_image_url)
			else:
				self.assertEqual(feature.get_popup_image_url(), '')

			if feature.banner_image:
				correct_banner_image_url = get_thumbnailer(feature.banner_image)['banner'].url
				self.assertEqual(feature.get_banner_image_url(), correct_banner_image_url)
			else:
				self.assertEqual(feature.get_banner_image_url(), '')

			if feature.popup_audio_file:
				correct_audio_file_url = feature.popup_audio_file.url
				self.assertEqual(feature.self.popup_audio_file.url, correct_audio_file_url)


class PointModelTestCase(AbstractFeatureModelTestCase):
	"""Points"""


class LineModelTestCase(AbstractFeatureModelTestCase):
	"""Lines"""


class PolygonModelTestCase(AbstractFeatureModelTestCase):
	"""Polygons"""


class AbstractAttachmentModelTestCase(TestCase):
	"""Attachment tests. As with features, Documents, Images, and AudioFiles all descend from the AbstractAttachement class. However, all are covered by the mehtods here."""

	def create_test_point(self):
		point = Point(0,0)
		return MmtPoint(name='test point', geom=point)

	def create_document(self):

		point = self.create_test_point()
		point.save()

		return Document.objects.create(
			title = 'test document',
			body = '<p>A test document<script>function a_nasty_script() { doing_something_naasty(); }</script></p>',
			point = point
		)

	def create_image(self):

		point = self.create_test_point()
		point.save()

		test_img = SimpleUploadedFile(name='Walter_Benjamin.jpg', content=open('mmt_map/Walter_Benjamin.jpg', 'rb').read(), content_type='image/jpeg')

		return Image.objects.create(
			title = 'test image',
			file = test_img,
			description = '<p>A test image<script>function a_nasty_script() { doing_something_naasty(); }</script></p>',
			point = point
		)

	def create_audio_file(self):
		point = self.create_test_point()
		point.save()

		test_audio_file = SimpleUploadedFile(name='Songs_of_innocence_and_experience_the_ecchoing_green_blake.mp3', content=open('mmt_map/Songs_of_innocence_and_experience_the_ecchoing_green_blake.mp3', 'rb').read(), content_type='audio/mpeg')

		return AudioFile.objects.create(
			title = 'test audio file',
			file = File(file=test_audio_file).save(),
			point = point
			)


	def test_attachment_creation(self):
		# Create an attachement of the of the correct type depending on which child model is being tested

		attachment = None

		if (isinstance(self, DocumentModelTestCase)):
			attachment = self.create_document()
		elif (isinstance(self, ImageModelTestCase)):
			attachment = self.create_image()
		elif (isinstance(self, AudioFileModelTestCase)):
			attachment = self.create_audio_file()

		# Don't run the test on an the abstract test case
		if attachment is not None:
			if hasattr(attachment, 'body'):
				# Test that the html has been cleaned properly
				self.assertNotEqual(attachment.body, attachment.body_processed)
			if hasattr(attachment, 'description'):
				cleaned_description = '&lt;p&gt;A test image&lt;script&gt;function a_nasty_script() { doing_something_naasty(); }&lt;/script&gt;&lt;/p&gt;'

				self.assertEqual(attachment.description, cleaned_description)




class DocumentModelTestCase(AbstractAttachmentModelTestCase):
	"""Documents"""

class ImageModelTestCase(AbstractAttachmentModelTestCase):
	"""Documents"""

class AudioFileModelTestCase(AbstractAttachmentModelTestCase):
	"""Documents"""


		
# View Tests
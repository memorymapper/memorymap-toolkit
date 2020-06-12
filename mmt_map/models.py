# Django Core
from django.contrib.gis.db import models
from django.contrib.auth.models import User

# Third party Django apps
from colorful.fields import RGBColorField
from easy_thumbnails.files import get_thumbnailer
from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField

# Other modules
import bleach
import markdown
import html2text
import re


def feature_directory_path(instance, filename):
	"""Function to ensure image files will be uploaded to /uploads/features/<feature.id>/filename"""
	try:
		feature = instance.feature
		return 'uploads/features/{0}/{1}'.format(feature.id, filename)
	except:
		return 'uploads/features/{0}/{1}'.format(instance.id, filename)


class Theme(models.Model):
	"""Feature categories"""
	name = models.CharField(max_length=128)
	color = RGBColorField(default='#4a62b1')

	def __str__(self):
		return self.name


class AbstractFeature(models.Model):
	"""The model class from which all feature objects derive"""
	name = models.CharField(max_length=140)
	theme = models.ForeignKey(Theme, blank=True, null=True, on_delete=models.SET_NULL)
	banner_image = models.ImageField(upload_to=feature_directory_path, null=True, blank=True, verbose_name='Banner Image')
	banner_image_copyright = models.CharField(max_length=240, blank=True)
	popup_image = models.ImageField(upload_to=feature_directory_path, null=True, blank=True)
	popup_audio_title = models.CharField(max_length=128, blank=True)
	popup_audio_slug = models.SlugField(max_length=128, blank=True)
	popup_audio_file = FilerFileField(null=True, blank=True, related_name='%(app_label)s_%(class)s_popup_audio_file', on_delete=models.SET_NULL)
	weight = models.FloatField(default=1)

	def get_type(self):
		return self.__class__.__name__.lower()

	def get_color(self):
		if self.theme:
			return self.theme.color
		else:
			return ''

	def get_popup_image_url(self):
		if self.popup_image:
			return get_thumbnailer(self.popup_image)['site_small'].url
		else:
			return ''

	def get_popup_audio_file_url(self):
		if self.popup_audio_file:
			return self.popup_audio_file.url

	def get_banner_image_url(self):
		if self.banner_image:
			return get_thumbnailer(self.banner_image)['banner'].url
		else:
			return ''

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		feature_type = self.get_type()
		return '/?feature_type=' + feature_type + '&id=' + str(self.id)

	class Meta:
		abstract = True


class Point(AbstractFeature):
 	"""A point"""
 	geom = models.PointField(verbose_name='Coordinates')


class Polygon(AbstractFeature):
 	"""A polygon"""
 	geom = models.MultiPolygonField(verbose_name='Geometry')


class Line(AbstractFeature):
 	"""A line"""
 	geom = models.MultiLineStringField(verbose_name='Line Geometry')


class AbstractAttachment(models.Model):
	"""The base class from which all attachments derive"""
	point = models.ForeignKey(Point, related_name='point_%(class)ss', null=True, blank=True, on_delete=models.SET_NULL)
	polygon = models.ForeignKey(Polygon, related_name='polygon_%(class)ss', null=True, blank=True, on_delete=models.SET_NULL)
	line = models.ForeignKey(Line, related_name='line_%(class)ss', null=True, blank=True, on_delete=models.SET_NULL)
	author = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_author', null=True, on_delete=models.SET_NULL)
	title = models.CharField(max_length=128)
	slug = models.SlugField(max_length=128, blank=True)
	order = models.PositiveSmallIntegerField(default=0)
	created = models.DateField(auto_now_add=True, null=True, blank=True)
	last_edited = models.DateField(auto_now=True, null=True, blank=True)
	published = models.BooleanField(default=False)

	def __str__(self):
		return self.title

	def get_type(self):
		return self.__class__.__name__.lower()

	class Meta:
		abstract = True


class Document(AbstractAttachment):
	"""A text document associated with a map feature"""	
	body = RichTextUploadingField(blank=False)
	body_processed = models.TextField(null=True, blank=True)
	
	def save(self, *args, **kwargs):
		"""Sanitize html input from users and add footnotes"""
		# Clean the html
		self.body = bleach.clean(self.body, tags=['p', 'b', 'strong', 'em', 'img', 'a', 'blockquote', 'i', 'li', 'ul', 'ol', 'h2', 'h3', 'h4', 'br', 'hr'], attributes={'img': ['alt', 'src', 'style'], 'a': ['href', 'target']}, styles=['width', 'height'])
		# Convert HTML to Markdown so you can run the footnote filter on it, then save as self.body_processed, which is what gets displayed on the site
		h = html2text.HTML2Text()
		h.ignore_images = False
		body_markdown = h.handle(self.body)
		self.body_processed = markdown.markdown(body_markdown, extensions=['markdown.extensions.footnotes'])
		super(Document, self).save(*args, **kwargs)


class Image(AbstractAttachment):
	"""An image associated with a map feature"""
	file = models.ImageField(upload_to=feature_directory_path, null=True, blank=False, verbose_name='Image')
	description = RichTextField(null=True, blank=True)
	copyright = models.CharField(blank=True, max_length=140)
	
	def save(self, *args, **kwargs):
		"""Bleach the description, Update the 'count' attribute of the feature"""
		self.description = bleach.clean(self.description, tags=['strong', 'em', 'a'], attributes={'a': ['href']})
		super(Image, self).save(*args, **kwargs)


class AudioFile(AbstractAttachment):
	"""An audio file associated with a map feature"""
	file = FilerFileField(null=True, blank=True, related_name='%(app_label)s_%(class)s_audio_file', on_delete=models.SET_NULL)


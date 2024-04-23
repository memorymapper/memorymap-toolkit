# Django Core
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import m2m_changed

# Third party Django apps
from colorful.fields import RGBColorField
from easy_thumbnails.files import get_thumbnailer
from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from taggit.models import Tag
from django_extensions.db.fields import AutoSlugField

# Other modules
import bleach
import markdown
import html2text
import re
import uuid


def feature_directory_path(instance, filename):
	"""Helper function to ensure images are saved in a sensible place in the uploads directory"""
	if hasattr(instance, 'name'):
		return 'uploads/features/{0}/{1}'.format(slugify(instance.name), filename)
	elif hasattr(instance, 'title'):
		return 'uploads/features/{0}/{1}'.format(slugify(instance.title), filename)


class Theme(models.Model):
	"""Feature categories"""
	name = models.CharField(max_length=128)
	color = RGBColorField(default='#4a62b1')

	def __str__(self):
		return self.name


class TagList(models.Model):
	"""A list of tag instances for display in a dropdown in the frontend"""
	name = models.CharField(max_length=64)
	tags = models.ManyToManyField(Tag)
	published = models.BooleanField(default=False)
	order = models.PositiveSmallIntegerField(default=0)

	def __str__(self):
		return self.name


class AbstractFeature(models.Model):
	"""The model class from which all feature objects derive"""
	name = models.CharField(max_length=140)
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	description = models.CharField(max_length=300, blank=True)
	theme = models.ForeignKey(Theme, blank=True, null=True, on_delete=models.SET_NULL)
	banner_image = models.ImageField(upload_to=feature_directory_path, null=True, blank=True, verbose_name='Banner Image')
	banner_image_copyright = models.CharField(max_length=240, blank=True)
	popup_image = models.ImageField(upload_to=feature_directory_path, null=True, blank=True)
	thumbnail_url = models.CharField(max_length=300, blank=True)
	popup_audio_title = models.CharField(max_length=128, blank=True)
	popup_audio_slug = models.SlugField(max_length=128, blank=True)
	popup_audio_file = FilerFileField(null=True, blank=True, related_name='%(app_label)s_%(class)s_popup_audio_file', on_delete=models.SET_NULL)
	weight = models.FloatField(default=1)
	tags = TaggableManager(blank=True)
	# When the feature is saved, the tags attached to it are stored as a string so they can be easily serialised as mapbox vector tiles
	tag_str = models.CharField(max_length=256, blank=True)
	published = models.BooleanField(default=False)
	# MVT and GeoJSON can't have nested values as properties, so the slugs of attachments are concatenated as a comma-separated string for consumption in Mapbox / Mapblibre
	attachments = models.CharField(max_length=768, blank=True)


	def get_type(self):
		return self.__class__.__name__.lower()

	# The get_*_url functions build the urls which are used in the API representation of a feature

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

	def get_absolute_url(self):
		feature_type = self.get_type()
		return '/?feature_type=' + feature_type + '&id=' + str(self.id)
	
	def get_color(self):
		if (self.theme):
			return self.theme.color
		else:
			return '#4a62b1'

	def __str__(self):
		return self.name

	class Meta:
		abstract = True


class Point(AbstractFeature):
	"""A point"""
	geom = models.PointField(verbose_name='Coordinates')

	def save(self, *args, **kwargs):
		# Model has to be saved first to access the tags
		super(Point, self).save(*args, **kwargs)
		self.tag_str = ', '.join(self.tags.names())
		# The hover thumbnail url needs to be saved in the DB because it needs to be accessed from the MVTs, not the API
		if self.popup_image:
			thumbnail_url = get_thumbnailer(self.popup_image)['hover_thumb'].url
			self.thumbnail_url = thumbnail_url
		if self.documents.filter(published=True).count() > 0:
			self.attachments = ','.join([d.slug for d in self.documents.filter(published=True)])
		super(Point, self).save(*args, **kwargs)



class Polygon(AbstractFeature):
	"""A polygon"""
	geom = models.MultiPolygonField(verbose_name='Geometry')

	def save(self, *args, **kwargs):
		if self.id:
			self.tag_str = ', '.join(self.tags.names())
			# The hover thumbnail url needs to be saved in the DB because it needs to be accessed from the MVTs, not the API
			if self.popup_image:
				thumbnail_url = get_thumbnailer(self.popup_image)['hover_thumb'].url
				self.thumbnail_url = thumbnail_url
			if self.documents.all().count() > 0:
				self.attachments = ','.join([d.slug for d in self.documents.all()])
		super(Polygon, self).save(*args, **kwargs)


class Line(AbstractFeature):
	"""A line"""
	geom = models.MultiLineStringField(verbose_name='Line Geometry')

	def save(self, *args, **kwargs):
		super(Line, self).save(*args, **kwargs)
		self.tag_str = ', '.join(self.tags.names())
		# The hover thumbnail url needs to be saved in the DB because it needs to be accessed from the MVTs, not the API
		if self.popup_image:
			thumbnail_url = get_thumbnailer(self.popup_image)['hover_thumb'].url
			self.thumbnail_url = thumbnail_url
		if self.documents.all().count() > 0:
			self.attachments = ','.join([d.slug for d in self.documents.all()])
		super(Line, self).save(*args, **kwargs)


def tags_changed(sender, **kwargs):
	"""Helper function to update the tag_str field on features when tags are changed."""
	action = kwargs['action']
	instance = kwargs['instance']
	model = kwargs['model']

	if (model == Tag):
		tags = ', '.join(instance.tags.names())
		instance.tag_str = tags
		instance.save()

m2m_changed.connect(tags_changed, sender=Point.tags.through)
m2m_changed.connect(tags_changed, sender=Line.tags.through)
m2m_changed.connect(tags_changed, sender=Polygon.tags.through)


class AbstractAttachment(models.Model):
	"""The base class from which all attachments derive"""
	point = models.ForeignKey(Point, related_name='%(class)ss', null=True, blank=True, on_delete=models.SET_NULL)
	polygon = models.ForeignKey(Polygon, related_name='%(class)ss', null=True, blank=True, on_delete=models.SET_NULL)
	line = models.ForeignKey(Line, related_name='%(class)ss', null=True, blank=True, on_delete=models.SET_NULL)
	author = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_author', null=True, on_delete=models.SET_NULL)
	title = models.CharField(max_length=128)
	slug = AutoSlugField(populate_from='title')
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
		ordering = ['order']


class Document(AbstractAttachment):
	"""A text document associated with a map feature"""	
	body = RichTextUploadingField(blank=False)
	body_processed = models.TextField(null=True, blank=True)
	
	def save(self, *args, **kwargs):
		"""Sanitize html input from users and add footnotes"""
		# Clean the html
		self.body = bleach.clean(self.body, tags=['p', 'b', 'strong', 'em', 'img', 'a', 'blockquote', 'i', 'li', 'ul', 'ol', 'h2', 'h3', 'h4', 'br', 'hr', 'iframe', 'u'], attributes={'img': ['alt', 'src', 'style'], 'a': ['href', 'target'], 'iframe': ['width', 'height', 'src', 'allow', 'frameborder']}, styles=['width', 'height'])
		
		## Todo: Footnotes filter -- disabled to enable bold and italics and underlines. Needs to be re-written and reactivated.
		
		# Convert HTML to Markdown so you can run the footnote filter on it, then save as self.body_processed, which is what gets displayed on the site.
		#h = html2text.HTML2Text()
		#h.ignore_images = False
		#h.unicode_snob = True
		# body_markdown = h.handle(self.body)
		# self.body_processed = markdown.markdown(body_markdown, extensions=['markdown.extensions.footnotes'])
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

	def get_audio_file_url(self):
		if self.file:
			return self.file.url


class MapLayer(models.Model):
	"""Additional raster map layers for your map"""
	name = models.CharField(max_length=64)
	tilejson_url = models.URLField(max_length=256)
	slug = AutoSlugField(populate_from='name')

	def __str__(self):
		return self.name

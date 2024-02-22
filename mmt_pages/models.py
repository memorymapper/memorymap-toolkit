# Django Core
from django.db import models
from django.urls import reverse

# Third party Django apps
from ckeditor_uploader.fields import RichTextUploadingField
from django_extensions.db.fields import AutoSlugField

# Other modules
import bleach

def page_directory_path(instance, filename):
	"""Helper function to ensure images are saved in a sensible place in the uploads directory"""
	if hasattr(instance, 'slug'):
		return 'uploads/pages/{0}/{1}'.format(instance.slug, filename)

class Page(models.Model):
	"""An HTML page"""
	title = models.CharField(max_length=140)
	slug = AutoSlugField(populate_from='title')
	body = RichTextUploadingField(blank=True, null=True)
	order = models.PositiveSmallIntegerField(default=0)
	is_front_page = models.BooleanField(default=False)
	is_instructions = models.BooleanField(default=False)
	# Banner image - for use for the front page modal
	banner_image = models.ImageField(upload_to=page_directory_path, null=True, blank=True, verbose_name='Banner Image')

	def __unicode__(self):
		return self.title

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('page', args=[self.slug])

	def switch_front_page(self):
		"""Checks if the current page has been set as the front page, and if so, find if there is another
		and un-front-pagify it."""
		if (self.is_front_page):
			try:
				curr_front_page = Page.objects.filter(is_front_page=True).exclude(id=self.id)[0]
				curr_front_page.is_front_page = False
				curr_front_page.save()
			except:
				pass

	def switch_instructions(self):
		"""Checks if there's already an instructions page, as above..."""
		if (self.is_instructions):
			try:
				curr_instructions = Page.objects.filter(is_instructions=True).exlude(id=self.id)[0]
				curr_instructions.is_instructions = False
				curr_instructions.save()
			except:
				pass

	def save(self, *args, **kwargs):
		# Clean the html
		self.body = bleach.clean(self.body, tags=['p', 'b', 'strong', 'em', 'img', 'a', 'blockquote', 'i', 'li', 'ul', 'ol', 'h2', 'h3', 'h4', 'br', 'hr', 'iframe'], attributes={'img': ['alt', 'src', 'style'], 'a': ['href', 'target'], 'iframe': ['width', 'height', 'src', 'allow', 'frameborder']}, styles=['width', 'height', 'float'])
		self.switch_front_page()
		self.switch_instructions()
		super(Page, self).save(*args, **kwargs)

	class Meta:
		ordering = ['order']


class Section(models.Model):
	"""A section of a page"""
	title = models.CharField(max_length=140)
	slug = AutoSlugField(populate_from='title')
	body = RichTextUploadingField(blank=True, null=True)
	order = models.PositiveSmallIntegerField(default=0)
	page = models.ForeignKey(Page, related_name='sections', on_delete=models.CASCADE, null=True)

	def __unicode__(self):
		return self.title
	
	def save(self, *args, **kwargs):
		# Clean the html
		self.body = bleach.clean(self.body, tags=['p', 'b', 'strong', 'em', 'img', 'a', 'blockquote', 'i', 'li', 'ul', 'ol', 'h2', 'h3', 'h4', 'br', 'hr', 'iframe'], attributes={'img': ['alt', 'src', 'style'], 'a': ['href', 'target'], 'iframe': ['width', 'height', 'src', 'allow', 'frameborder']}, styles=['width', 'height', 'float'])
		super(Section, self).save(*args, **kwargs)
	
	class Meta:
		ordering = ['order']
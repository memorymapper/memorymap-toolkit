# Django Core
from django.db import models
from django.urls import reverse

# Third party Django apps
from ckeditor_uploader.fields import RichTextUploadingField

# Other modules
import bleach

class Page(models.Model):
	"""An HTML page"""
	title = models.CharField(max_length=140)
	slug = models.SlugField()
	body = RichTextUploadingField(blank=True, null=True)
	order = models.PositiveSmallIntegerField(default=0)

	def __unicode__(self):
		return self.title

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('page', args=[self.slug])

	def save(self, *args, **kwargs):
		# Clean the html
		self.body = bleach.clean(self.body, tags=['p', 'b', 'strong', 'em', 'img', 'a', 'blockquote', 'i', 'li', 'ul', 'ol', 'h2', 'h3', 'h4', 'br', 'hr', 'iframe'], attributes={'img': ['alt', 'src', 'style'], 'a': ['href', 'target'], 'iframe': ['width', 'height', 'src', 'allow', 'frameborder']}, styles=['width', 'height'])
		super(Page, self).save(*args, **kwargs)

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
	is_front_page = models.BooleanField(default=False)

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

	def save(self, *args, **kwargs):
		# Clean the html
		self.body = bleach.clean(self.body, tags=['p', 'b', 'strong', 'em', 'img', 'a', 'blockquote', 'i', 'li', 'ul', 'ol', 'h2', 'h3', 'h4', 'br', 'hr', 'iframe'], attributes={'img': ['alt', 'src', 'style'], 'a': ['href', 'target'], 'iframe': ['width', 'height', 'src', 'allow', 'frameborder']}, styles=['width', 'height'])
		self.switch_front_page()
		super(Page, self).save(*args, **kwargs)

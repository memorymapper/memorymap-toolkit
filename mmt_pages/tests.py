# Django core
from django.test import TestCase

# 3rd party Django apps

# Memory Map Toolkit

from .models import Page

# Other modules


class PageModelTestCase(TestCase):
	"""Page tests"""
	
	def create_page(self):
		return Page.objects.create(title='test theme', body='<p>A test document <script>function do_something_nasty() { malicious_code(); }</script>')

	def test_page_creation(self):
		"""Make sure a page is created properly"""

		page = self.create_page()
		self.assertTrue(isinstance(page, Page))

		# Test the html was cleaned properly
		cleaned_body = '<p>A test document &lt;script&gt;function do_something_nasty() { malicious_code(); }&lt;/script&gt;</p>'
		self.assertEqual(page.body, cleaned_body)
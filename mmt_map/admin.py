# Django core
from django.contrib.gis import admin

# Memory Map Toolkit
from .models import Theme, Point, Polygon, Line, Document, Image, AudioFile
from .forms import PointForm, PolygonForm, LineForm

# 3rd Party

class DocumentInline(admin.StackedInline):
	model = Document
	prepopulated_fields = {"slug": ("title",)}
	fields = ['title', 'slug', 'order', 'published', 'body',]
	extra = 0

class ImageInline(admin.StackedInline):
	model = Image
	prepopulated_fields = {"slug": ("title",)}
	fields = ['title', 'slug', 'order', 'published', 'file', 'description', 'copyright',]
	extra = 0

class AudioFileInline(admin.StackedInline):
	model = AudioFile
	prepopulated_fields = {"slug": ("title",)}
	fields =['title', 'slug', 'order', 'published', 'file',]
	extra = 0



class PointAdmin(admin.GeoModelAdmin):
	form = PointForm

	inlines = [
		DocumentInline,
		ImageInline,
		AudioFileInline,
	]

	list_display = ['name', 'theme', 'weight', 'published']
	list_editable = ['theme', 'weight', 'published']

	class Meta:
		model = Point


class PolygonAdmin(admin.GeoModelAdmin):
	form = PolygonForm

	inlines = [
		DocumentInline,
		ImageInline,
		AudioFileInline,
	]

	list_display = ['name', 'theme', 'weight', 'published']
	list_editable = ['theme', 'weight', 'published']

	class Meta:
		model = Polygon


class LineAdmin(admin.GeoModelAdmin):
	form = LineForm

	inlines = [
		DocumentInline,
		ImageInline,
		AudioFileInline,
	]

	list_display = ['name', 'theme', 'weight', 'published']
	list_editable = ['theme', 'weight', 'published']

	class Meta:
		model = Line


admin.site.register(Theme)
admin.site.register(Point, PointAdmin)
admin.site.register(Polygon, PolygonAdmin)
admin.site.register(Line, LineAdmin)
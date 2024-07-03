# Django core
from django.contrib.gis import admin

# Memory Map Toolkit
from .models import Theme, Point, Polygon, Line, Document, Image, AudioFile, TagList, MapLayer, MultiPoint
from .forms import PointForm, PolygonForm, LineForm, MultiPointForm

# 3rd Party


def set_read_only_fields(request, fields):
	"""
	Stops users who aren't superusers or members of a group called 'Editors' in the admin site from changing the publication status of a document or map geometry by setting the 'published' field to read-only.
	"""
	fields = list(fields)
	if not request.user.groups.filter(name='Editors').exists():
		fields += ['published']
	if request.user.is_superuser:
		fields.clear()
	return fields


class DocumentInline(admin.StackedInline):
	model = Document
	# prepopulated_fields = {"slug": ("title",)}
	fields = ['title', 'order', 'published', 'body',]
	extra = 1

	def get_readonly_fields(self, request, obj=None):
		fields = super(DocumentInline, self).get_readonly_fields(request, obj)
		return set_read_only_fields(request, fields)


class ImageInline(admin.StackedInline):
	model = Image
	# prepopulated_fields = {"slug": ("title",)}
	fields = ['title', 'order', 'published', 'file', 'description', 'copyright',]
	extra = 1

	def get_readonly_fields(self, request, obj=None):
		fields = super(ImageInline, self).get_readonly_fields(request, obj)
		return set_read_only_fields(request, fields)


class AudioFileInline(admin.StackedInline):
	model = AudioFile
	# prepopulated_fields = {"slug": ("title",)}
	fields =['title', 'order', 'published', 'file',]
	extra = 1

	def get_readonly_fields(self, request, obj=None):
		fields = super(AudioFileInline, self).get_readonly_fields(request, obj)
		return set_read_only_fields(request, fields)


@admin.action(description="Publish selected features")
def publish(modeladmin, request, queryset):
	queryset.update(published=True)

@admin.action(description="Unpublish selected features")
def unpublish(modeladmin, request, queryset):
	queryset.update(published=False)


class PointAdmin(admin.GeoModelAdmin):
	form = PointForm

	inlines = [
		DocumentInline,
		ImageInline,
		AudioFileInline,
	]

	list_display = ['name', 'uuid', 'theme', 'weight', 'published']
	list_editable = ['theme', 'weight', 'published']

	prepopulated_fields = {"popup_audio_slug": ("popup_audio_title",)}

	search_fields = ['name']

	actions = [publish, unpublish]

	class Meta:
		model = Point

	def get_readonly_fields(self, request, obj=None):
		fields = super(PointAdmin, self).get_readonly_fields(request, obj)
		return set_read_only_fields(request, fields)


class MultiPointAdmin(admin.GeoModelAdmin):
	form = MultiPointForm

	inlines = [
		DocumentInline,
		ImageInline,
		AudioFileInline,
	]

	list_display = ['name', 'uuid', 'theme', 'weight', 'published']
	list_editable = ['theme', 'weight', 'published']

	prepopulated_fields = {"popup_audio_slug": ("popup_audio_title",)}

	search_fields = ['name']

	actions = [publish, unpublish]

	class Meta:
		model = MultiPoint

	def get_readonly_fields(self, request, obj=None):
		fields = super(MultiPointAdmin, self).get_readonly_fields(request, obj)
		return set_read_only_fields(request, fields)


class PolygonAdmin(admin.GeoModelAdmin):
	form = PolygonForm

	inlines = [
		DocumentInline,
		ImageInline,
		AudioFileInline,
	]

	list_display = ['name', 'theme', 'weight', 'published', 'uuid']
	list_editable = ['theme', 'weight', 'published']

	prepopulated_fields = {"popup_audio_slug": ("popup_audio_title",)}

	search_fields = ['name']

	actions = [publish, unpublish]

	class Meta:
		model = Polygon

	def get_readonly_fields(self, request, obj=None):
		fields = super(PolygonAdmin, self).get_readonly_fields(request, obj)
		return set_read_only_fields(request, fields)


class LineAdmin(admin.GeoModelAdmin):
	form = LineForm

	inlines = [
		DocumentInline,
		ImageInline,
		AudioFileInline,
	]

	list_display = ['name', 'theme', 'weight', 'published']
	list_editable = ['theme', 'weight', 'published']

	prepopulated_fields = {"popup_audio_slug": ("popup_audio_title",)}

	search_fields = ['name']

	actions = [publish, unpublish]

	class Meta:
		model = Line

	def get_readonly_fields(self, request, obj=None):
		fields = super(LineAdmin, self).get_readonly_fields(request, obj)
		return set_read_only_fields(request, fields)


class ThemeAdmin(admin.ModelAdmin):
	list_display = ['name', 'color']
	list_editable = ['color']

	class Meta:
		model = Theme


class MapLayerAdmin(admin.ModelAdmin):
	list_display = ['name', 'order']
	list_editable = ['order']
	
	class Meta:
		model = MapLayer


admin.site.register(Theme, ThemeAdmin)
admin.site.register(Point, PointAdmin)
# MultiPoint Admin is enabled, but the drawing interface for adding them doesn't work. But you still need to be able to 
# edit the content...
admin.site.register(MultiPoint, MultiPointAdmin)
admin.site.register(Polygon, PolygonAdmin)
admin.site.register(Line, LineAdmin)
admin.site.register(TagList)
admin.site.register(MapLayer, MapLayerAdmin)
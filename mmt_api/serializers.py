# Django core

# Third party Django apps
from rest_framework import routers, serializers, viewsets
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometrySerializerMethodField, GeometryField

# Other Python modules

# Memory Map Toolkit
from mmt_map.models import AbstractFeature, Point, Line, Polygon, Document, Image, AudioFile, Theme
from mmt_pages.models import Page


# Map serializers

class AbstractFeatureSerializer(GeoFeatureModelSerializer):
	feature_type = serializers.CharField(source='get_type', read_only=True)
	theme = serializers.StringRelatedField()
	popup_image = serializers.CharField(source='get_popup_image_url', read_only=True)
	popup_audio_file = serializers.CharField(source='get_popup_audio_file_url', read_only=True)
	banner_image = serializers.CharField(source='get_banner_image_url', read_only=True)

class PointSerializer(AbstractFeatureSerializer):
	class Meta:
		model = Point
		geo_field = 'geom'
		fields = ('id', 'feature_type', 'name', 'theme', 'popup_image', 'banner_image', 'weight', 'popup_audio_file', 'popup_audio_title', 'banner_image_copyright', 'popup_audio_slug',)

class PolygonSerializer(AbstractFeatureSerializer):
	class Meta:
		model = Polygon
		geo_field = 'geom'
		fields = ('id', 'feature_type', 'name', 'theme', 'popup_image', 'banner_image', 'weight', 'popup_audio_file', 'popup_audio_title', 'banner_image_copyright', 'popup_audio_slug',)

class LineSerializer(AbstractFeatureSerializer):
	class Meta:
		model = Line
		geo_field = 'geom'
		fields = ('id', 'feature_type', 'name', 'theme', 'popup_image', 'banner_image', 'weight', 'popup_audio_file', 'popup_audio_title', 'banner_image_copyright', 'popup_audio_slug',)



class DocumentSerializer(serializers.ModelSerializer):
	attachment_type = serializers.CharField(source='get_type', read_only=True)
	class Meta:
		model = Document
		fields = ('attachment_type', 'title', 'body_processed', 'order', 'slug')

class ImageSerializer(serializers.ModelSerializer):
	attachment_type = serializers.CharField(source='get_type', read_only=True)
	class Meta:
		model = Image
		fields = ('attachment_type', 'title', 'file', 'description', 'copyright', 'slug')

class AudioFileSerializer(serializers.ModelSerializer):
	attachment_type = serializers.CharField(source='get_type', read_only=True)
	class Meta:
		model = AudioFile
		fields = ('attachment_type', 'title', 'slug')



class PointDetailSerializer(serializers.ModelSerializer):
	point_documents = DocumentSerializer(many=True, read_only=True)
	point_images = ImageSerializer(many=True, read_only=True)
	point_audiofiles = AudioFileSerializer(many=True, read_only=True)

	class Meta:
		model = Point
		fields = ('name', 'point_documents', 'point_images', 'point_audiofiles', 'thumbnail_copyright',)

class PolygonDetailSerializer(serializers.ModelSerializer):
	polygon_documents = DocumentSerializer(many=True, read_only=True)
	polygon_images = ImageSerializer(many=True, read_only=True)
	polygon_audiofiles = AudioFileSerializer(many=True, read_only=True)

	class Meta:
		model = Polygon
		fields = ('name', 'polygon_documents', 'polygon_images', 'polygon_audiofiles', 'thumbnail_copyright',)

class LineDetailSerializer(serializers.ModelSerializer):
	line_documents = DocumentSerializer(many=True, read_only=True)
	line_images = ImageSerializer(many=True, read_only=True)
	line_audiofiles = AudioFileSerializer(many=True, read_only=True)

	class Meta:
		model = Line
		fields = ('name', 'line_documents', 'line_images', 'line_audiofiles', 'thumbnail_copyright',)


# Other serializers

class PageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Page
		fields = ('title', 'slug', 'body',)


class PageLinkSerializer(serializers.ModelSerializer):
	class Meta:
		model = Page
		fields = ('title', 'slug', 'order',)

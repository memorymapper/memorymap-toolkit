# Django core
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from django.core.serializers import serialize
from django.http import JsonResponse
from django.db import connection

# Other Python modules
import json 

# Memory Map Toolkit
from mmt_map.models import Point, Line, Polygon, Theme, Document, Image, AudioFile
from mmt_pages.models import Page
from .serializers import PointSerializer, PolygonSerializer, LineSerializer, PointDetailSerializer, PolygonDetailSerializer, LineDetailSerializer, DocumentSerializer, PageSerializer, AudioFileSerializer, ImageSerializer, PageLinkSerializer


def feature(request, pk, source_layer):
	"""
	Returns a GeoJSON representation of a single feature
	"""

	feature = None
	serializer = None

	if source_layer == 'points':
		point = Point.objects.get(id=pk)
		serializer = PointSerializer(point)
	elif source_layer == 'polygons':
		poly = Polygon.objects.get(id=pk)
		serializer = PolygonSerializer(poly)
	elif source_layer == 'lines':
		line = Line.objects.get(id=pk)
		serializer = LineSerializer(line)

	return JsonResponse(serializer.data)



def feature_detail(request, pk, source_layer):
	"""
	Returns a JSON representation of a single feature and all of its attachements
	"""
	feature = None
	serializer = None

	if source_layer == 'points':
		point = Point.objects.get(id=pk)
		serializer = PointDetailSerializer(point)
	elif source_layer == 'polygons':
		polygon = Polygon.objects.get(id=pk)
		serializer = PolygonDetailSerializer(polygon)
	elif source_layer == 'lines':
		line = Line.objects.get(id=pk)
		serializer = LineDetailSerializer(line)

	return JsonResponse(serializer.data)



def feature_attachments(request, pk, source_layer):
	"""
	Returns a JSON representation of all of the attachements associated with a feature in the correct order
	"""

	if source_layer == 'points':
		feature = get_object_or_404(Point, id=pk)
		documents = Document.objects.filter(point=feature, published=True)
		images = Image.objects.filter(point=feature, published=True)
		audio = AudioFile.objects.filter(point=feature, published=True)
		feature_serializer = PointSerializer(feature)
	elif source_layer == 'polygons':
		feature = get_object_or_404(Polygon, id=pk)
		documents = Document.objects.filter(polygon=feature, published=True)
		images = Image.objects.filter(polygon=feature, published=True)
		audio = AudioFile.objects.filter(polygon=feature, published=True)
		feature_serializer = PolygonSerializer(feature)
	elif source_layer == 'lines':
		feature = get_object_or_404(Line, id=pk)
		documents = Document.objects.filter(line=feature, published=True)
		images = Image.objects.filter(line=feature, published=True)
		audio = AudioFile.objects.filter(line=feature, published=True)
		feature_serializer = LineSerializer(feature)

	attachments_base = {'documents': documents, 'images': images, 'audio': audio}

	attachments = []
	for key, value in attachments_base.items():
		for v in value:
			attachments.append(v)

	attachments = sorted(attachments, key=lambda attachment: attachment.order)

	attachments_json = []

	for a in attachments:
		if a.__class__.__name__.lower() == 'document':
			print('d')
			serializer = DocumentSerializer(a)
		elif a.__class__.__name__.lower() == 'image':
			serializer = ImageSerializer(a)
			print('i')
		elif a.__class__.__name__.lower() == 'audiofile':
			serializer = AudioFileSerializer(a)
			print('a')

		attachments_json.append(serializer.data)

	feature = feature_serializer.data

	feature['attachments'] = attachments_json

	return JsonResponse(feature, safe=False)



def document(request, pk):
	"""
	Returns a JSON representation of a single document
	"""
	document = Document.objects.get(id=pk)
	serializer = DocumentSerializer(document)

	return JsonResponse(serializer.data)


def page(request, slug):
	"""
	Returns a JSON representation of an information page
	"""

	page = Page.objects.get(slug=slug)
	serializer = PageSerializer(page)

	return JsonResponse(serializer.data)


def pages(request):
	"""
	Returns a JSON representation of all of the pages on the site
	"""

	pages = Page.objects.all()
	serializer = PageLinkSerializer(pages, many=True)

	return JsonResponse(serializer.data, safe=False)
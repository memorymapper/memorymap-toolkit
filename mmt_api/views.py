# Django core
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

# 3rd Party
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status

# Other Python modules
import json 

# Memory Map Toolkit
from mmt_map.models import Point, Line, Polygon, Theme, Document, Image, AudioFile
from mmt_pages.models import Page
from .serializers import PointSerializer, PolygonSerializer, LineSerializer, PointDetailSerializer, PolygonDetailSerializer, LineDetailSerializer, DocumentSerializer, PageSerializer, AudioFileSerializer, ImageSerializer, PageLinkSerializer


# Memorymapper exposes a read-only API allowing access to the data in a given Memory Map. 
# This is used throughout the web application, though we hope (subject to further 
# funding) to use this as the basis of the development of native mobile 
# applications to allow people to download content it and access it in areas where mobile 
# reception is poor.


@api_view()
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

	return Response(serializer.data)


@api_view()
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

	return Response(serializer.data)


@api_view()
def feature_list(request):
	"""
	Returns a paginated list of features (used for text only access to memory map content)
	"""

	points = Point.objects.filter(published=True)
	lines = Line.objects.filter(published=True)
	polygons = Polygon.objects.filter(published=True)

	points_serializer = PointSerializer(points, many=True)
	lines_serializer = LineSerializer(lines, many=True)
	polygons_serializer = PolygonSerializer(polygons, many=True)

	points_data = points_serializer.data
	lines_data = lines_serializer.data
	polygons_data = polygons_serializer.data

	features = points_data['features'] + lines_data['features'] + polygons_data['features']
	sorted_features = sorted(features, key=lambda x: x['properties']['name'])

	paginator = Paginator(sorted_features, 20)

	try:
		page = request.GET['page']

	except:
		page = 1

	if int(page) > paginator.num_pages:
		page = paginator.num_pages

	features_list = {
		'page': page,
		'totalPages': paginator.num_pages,
		'features': paginator.page(page).object_list
	}  

	return Response(features_list)


@api_view()
def search_features(request):
	"""
	Search features by title or tags. Returns a JSON list of results.
	"""

	try:
		search_string = request.GET['q']
	except:
		return Response('No search string', status=status.HTTP_404_NOT_FOUND)

	points = Point.objects.filter(Q(published=True), Q(name__icontains=search_string) | Q(tags__name__in=[search_string])).distinct()
	lines = Line.objects.filter(Q(published=True), Q(name__icontains=search_string) | Q(tags__name__in=[search_string])).distinct()
	polygons = Polygon.objects.filter(Q(published=True), Q(name__icontains=search_string) | Q(tags__name__in=[search_string])).distinct()

	points_serializer = PointSerializer(points, many=True)
	lines_serializer = LineSerializer(lines, many=True)
	polygons_serializer = PolygonSerializer(polygons, many=True)

	points_data = points_serializer.data
	lines_data = lines_serializer.data
	polygons_data = polygons_serializer.data

	features = points_data['features'] + lines_data['features'] + polygons_data['features']
	sorted_features = sorted(features, key=lambda x: x['properties']['name'])

	paginator = Paginator(sorted_features, 20)

	try:
		page = request.GET['page']

	except:
		page = 1

	if int(page) > paginator.num_pages:
		page = paginator.num_pages

	features_list = {
		'page': page,
		'totalPages': paginator.num_pages,
		'features': paginator.page(page).object_list
	} 

	return Response(features_list)


@api_view()
def get_features_by_theme(request):
	"""
	Returns a JSON list of features in a particular theme.
	"""

	try:
		theme = request.GET['theme']
	except:
		return Response('No theme id', status=status.HTTP_404_NOT_FOUND)

	points = Point.objects.filter(theme=theme)
	lines = Line.objects.filter(theme=theme)
	polygons = Polygon.objects.filter(theme=theme)

	points_serializer = PointSerializer(points, many=True)
	lines_serializer = LineSerializer(lines, many=True)
	polygons_serializer = PolygonSerializer(polygons, many=True)

	points_data = points_serializer.data
	lines_data = lines_serializer.data
	polygons_data = polygons_serializer.data

	features = points_data['features'] + lines_data['features'] + polygons_data['features']
	sorted_features = sorted(features, key=lambda x: x['properties']['name'])

	paginator = Paginator(sorted_features, 20)

	try:
		page = request.GET['page']

	except:
		page = 1

	if int(page) > paginator.num_pages:
		page = paginator.num_pages

	features_list = {
		'page': page,
		'totalPages': paginator.num_pages,
		'features': paginator.page(page).object_list
	} 

	return Response(features_list)



@api_view()
def get_features_by_tag(request):
	"""
	Returns a JSON list of features in a particular theme.
	"""

	try:
		tags = request.GET['tags'].split(',')
		print(tags)
	except:
		return Response('No tags', status=status.HTTP_404_NOT_FOUND)



	points = Point.objects.filter(tags__name__in=tags)
	lines = Line.objects.filter(tags__name__in=tags)
	polygons = Polygon.objects.filter(tags__name__in=tags)

	points_serializer = PointSerializer(points, many=True)
	lines_serializer = LineSerializer(lines, many=True)
	polygons_serializer = PolygonSerializer(polygons, many=True)

	points_data = points_serializer.data
	lines_data = lines_serializer.data
	polygons_data = polygons_serializer.data

	features = points_data['features'] + lines_data['features'] + polygons_data['features']
	sorted_features = sorted(features, key=lambda x: x['properties']['name'])

	paginator = Paginator(sorted_features, 20)

	try:
		page = request.GET['page']

	except:
		page = 1

	if int(page) > paginator.num_pages:
		page = paginator.num_pages

	features_list = {
		'page': page,
		'totalPages': paginator.num_pages,
		'features': paginator.page(page).object_list
	} 

	return Response(features_list)



@api_view()
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
			serializer = DocumentSerializer(a)
		elif a.__class__.__name__.lower() == 'image':
			serializer = ImageSerializer(a)
		elif a.__class__.__name__.lower() == 'audiofile':
			serializer = AudioFileSerializer(a)

		attachments_json.append(serializer.data)

	feature = feature_serializer.data

	feature['attachments'] = attachments_json

	return Response(feature)


@api_view()
def document(request, pk):
	"""
	Returns a JSON representation of a single document
	"""
	document = Document.objects.get(id=pk)
	serializer = DocumentSerializer(document)

	return Response(serializer.data)


@api_view()
def page(request, slug):
	"""
	Returns a JSON representation of an information page
	"""

	page = Page.objects.get(slug=slug)
	serializer = PageSerializer(page)

	return Response(serializer.data)

@api_view()
def pages(request):
	"""
	Returns a JSON representation of all of the pages on the site
	"""

	pages = Page.objects.all().order_by('order')
	serializer = PageLinkSerializer(pages, many=True)

	return Response(serializer.data)
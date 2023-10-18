# Django core
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.conf import settings

# 3rd Party
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status, filters
from constance import config
from rest_framework.generics import ListAPIView

# Other Python modules
import json 

# Memory Map Toolkit
from mmt_map.models import AbstractFeature, Point, Line, Polygon, Theme, Document, Image, AudioFile, TagList
from mmt_pages.models import Page
from .serializers import PointSerializer, PolygonSerializer, LineSerializer, PointDetailSerializer, PolygonDetailSerializer, LineDetailSerializer, DocumentSerializer, PageSerializer, AudioFileSerializer, ImageSerializer, PageLinkSerializer, ThemeSerializer, TagListSerializer, TersePointSerializer, TersePolygonSerializer, TerseLineSerializer


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
def feature_detail_by_uuid(request, uuid):
	"""
	Returns a JSON representation of a single feature and all of its attachements
	"""
	feature = None
	serializer = None

	try:
		feature = Point.objects.get(uuid=uuid)
		serializer = PointDetailSerializer(feature)
	except Point.DoesNotExist:
		pass
	
	try:
		feature = Polygon.objects.get(uuid=uuid)
		serializer = PolygonDetailSerializer(feature)
	except:
		pass

	try:
		feature = Line.objects.get(uuid=uuid)
		serializer = LineDetailSerializer(feature)
	except:
		pass

	if not feature:
		return Response('Feature not found', status=status.HTTP_404_NOT_FOUND)
	
	return Response(serializer.data)


@api_view()
def feature_by_uuid(request, uuid):
	"""
	Returns a JSON representation of a single feature and all of its attachements,
	or, alternatively, a compact version of the same
	"""

	terse = False

	try:
		terse = json.loads(request.GET.get('compact'))
	except Exception as err:
		terse = False

	feature = None
	serializer = None

	try:
		feature = Point.objects.get(uuid=uuid)
		if (terse):
			serializer = TersePointSerializer(feature)
		else:
			serializer = PointSerializer(feature)
	except Point.DoesNotExist:
		pass
	
	try:
		feature = Polygon.objects.get(uuid=uuid)
		if (terse):
			serializer = TersePolygonSerializer(feature)
		else:
			serializer = PolygonSerializer(feature)
	except:
		pass

	try:
		feature = Line.objects.get(uuid=uuid)
		if (terse):
			serializer = TerseLineSerializer(feature)
		else:
			serializer = LineSerializer(feature)
	except:
		pass

	if not feature:
		return Response('Feature not found', status=status.HTTP_404_NOT_FOUND)
	
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

	paginator = Paginator(sorted_features, 5)

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
def feature_attachments_by_uuid(request, uuid):
	"""
	Returns a JSON representation of a single feature and all of its attachements
	"""
	feature = None
	serializer = None

	try:
		feature = Point.objects.get(uuid=uuid)
		documents = Document.objects.filter(point=feature, published=True)
		images = Image.objects.filter(point=feature, published=True)
		audio = AudioFile.objects.filter(point=feature, published=True)
		feature_serializer = PointSerializer(feature)
	except Point.DoesNotExist:
		pass
	
	try:
		feature = Polygon.objects.get(uuid=uuid)
		documents = Document.objects.filter(polygon=feature, published=True)
		images = Image.objects.filter(polygon=feature, published=True)
		audio = AudioFile.objects.filter(polygon=feature, published=True)
		feature_serializer = PolygonSerializer(feature)
	except:
		pass

	try:
		feature = Line.objects.get(uuid=uuid)
		documents = Document.objects.filter(line=feature, published=True)
		images = Image.objects.filter(line=feature, published=True)
		audio = AudioFile.objects.filter(line=feature, published=True)
		feature_serializer = LineSerializer(feature)
	except:
		pass

	if not feature:
		return Response('Feature not found', status=status.HTTP_404_NOT_FOUND)

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
def feature_document_by_uuid(request, uuid, slug):
	feature = None
	

	try:
		feature = Point.objects.get(uuid=uuid)
		document = Document.objects.get(point=feature, slug=slug)
	except Point.DoesNotExist:
		pass
	
	try:
		feature = Polygon.objects.get(uuid=uuid)
		document = Document.objects.get(polygon=feature, slug=slug)
	except:
		pass

	try:
		feature = Line.objects.get(uuid=uuid)
		document = Document.objects.get(line=feature, slug=slug)
	except:
		pass

	if not feature:
		return Response('Feature not found', status=status.HTTP_404_NOT_FOUND)

	serializer = DocumentSerializer(document)

	return Response(serializer.data)

@api_view()
def document(request, pk):
	"""
	Returns a JSON representation of a single document
	"""
	document = Document.objects.get(id=pk)
	serializer = DocumentSerializer(document)

	return Response(serializer.data)


class DocumentList(ListAPIView):
	queryset = Document.objects.all()
	serializer_class = DocumentSerializer
	filter_backends = [filters.SearchFilter]
	search_fields = ['@body', '@title', '@point__name', '@polygon__name', '@line__name']


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


@api_view()
def front_page(request):
	"""
	A JSON representation of the front page
	"""
	try:
		page = Page.objects.filter(is_front_page=True)[0]
		serializer = PageSerializer(page)
		return Response(serializer.data)
	except:
		return Response('Page not found', status=status.HTTP_404_NOT_FOUND)


@api_view()
def site_config(request):
	"""
	Returns a JSON representation of the constance settings object and the URL of the styleJson object for the vector tiles. And the themes and the tags.
	TODO: take the themes and tags out and put them in separate API calls
	"""

	scheme = request.scheme
	host = request.get_host()

	tile_json_url = scheme + '://' + host + '/tiles/interactive.json'

	config_dict = {
		'SITE_TITLE': config.SITE_TITLE,
		'SITE_SUBTITLE': config.SITE_SUBTITLE,
		'LOGO_IMAGE': config.LOGO_IMAGE,
		'MAP_CENTER_LATITUDE': config.MAP_CENTER_LATITUDE,
		'MAP_CENTER_LONGITUDE': config.MAP_CENTER_LONGITUDE,
		'BOUNDS_SW_LATITUDE': config.BOUNDS_SW_LATITUDE,
		'BOUNDS_SW_LONGITUDE': config.BOUNDS_SW_LONGITUDE,
		'BOUNDS_NE_LATITUDE': config.BOUNDS_NE_LATITUDE,
		'BOUNDS_NE_LONGITUDE': config.BOUNDS_NE_LONGITUDE,
		'ZOOM': config.ZOOM,
		'MIN_ZOOM': config.MIN_ZOOM,
		'MAX_ZOOM': config.MAX_ZOOM,
		'BASE_MAP_STYLE_URL': config.BASE_MAP_STYLE_URL,
		'BASE_MAP_STYLE_FILE': config.BASE_MAP_STYLE_FILE,
		'MAPTILER_KEY': config.MAPTILER_KEY,
		'MAPBOX_KEY': config.MAPBOX_KEY,
		'SCALE': config.SCALE,
		'PITCH': config.PITCH,
		'BEARING': config.BEARING,
		'WELCOME_MESSAGE': config.WELCOME_MESSAGE,
		'TILE_JSON_URL': tile_json_url,
		'themes': {},
		'tagLists': {}
	}

	themes = Theme.objects.all()
	serializer = ThemeSerializer(themes, many=True)

	for theme in serializer.data:
		config_dict['themes'][theme['id']] = {
			'color': theme['color'],
			'name': theme['name'],
			'active': True
		}

	taglists = TagList.objects.filter(published=True). order_by('order')
	serializer = TagListSerializer(taglists, many=True)
	
	for tl in serializer.data:
		config_dict['tagLists'][tl['id']] = {
			'name': tl['name'],
			'tags': {}
		}
		for tag in tl['tags']:
			config_dict['tagLists'][tl['id']]['tags'][tag['id']] = {'name': tag['name'], 'slug': tag['slug'], 'active': True}
		


	return JsonResponse(config_dict)

@api_view()
def theme_list(request):
	"""
	Returns a list of themes
	"""
	themes = Theme.objects.all()
	serializer = ThemeSerializer(themes, many=True)

	return Response(serializer.data)


@api_view()
def search(request):
	"""
	Search everything
	"""

	try:
		search_string = request.GET['q']
		
	except:
		return Response('No search string', status=status.HTTP_404_NOT_FOUND)
	
	try:
		limit = int(request.GET['limit'])
	except:
		limit = 8

	try:
		query = SearchQuery(search_string, search_type='phrase')
		#vector = SearchVector('name__unaccent', 'tag_str')

		#points = Point.objects.annotate(rank=SearchRank(vector, query)).order_by('-rank').exclude(rank=0.0)[:limit]

		points = Point.objects.annotate(similarity = TrigramSimilarity('name__unaccent', search_string),).filter(similarity__gt=0.3).order_by('-similarity')[:limit]
		
		lines = Line.objects.annotate(similarity = TrigramSimilarity('name__unaccent', search_string),).filter(similarity__gt=0.3).order_by('-similarity')[:limit]

		polygons = Polygon.objects.annotate(similarity = TrigramSimilarity('name__unaccent', search_string),).filter(similarity__gt=0.3).order_by('-similarity')[:limit]

		vector = SearchVector('body', weight='A') + SearchVector('title', weight='B') + SearchVector('point__name', weight='C')

		documents = Document.objects.annotate(rank=SearchRank(vector, query)).order_by('-rank').exclude(rank=0.0)[:limit]


		results = []

		for p in points:
			try:
				results.append(
					{
						'id': p.id,
						'name': p.name,
						'uuid': p.uuid,
						'category': 'Place',
						'slug': p.documents.all()[0].slug,
						'description': p.description,
						'similarity': p.similarity
					}
				)
			except:
				continue
		
		for d in documents:
			try:
				results.append(
					{
						'id': d.id,
						'name': d.title,
						'uuid': d.point.uuid,
						'category': 'Document',
						'slug': d.slug,
						'place': d.point.name,
						'rank': d.rank
					}
				)
			except:
				continue
		
		# TODO: Create a SearchResultsSerializer, and return the data with that instead so it's browsable in the REST api web interface
		return JsonResponse({'results': results})
	
	except Exception as err:
		return Response('Server Error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
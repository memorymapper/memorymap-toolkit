# Django core
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from django.core.serializers import serialize
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.cache import cache_page
from django.contrib.gis.geos import GEOSGeometry

# Other Python modules
import json 
from datetime import datetime

# Third Party Django apps
from constance import config

# Memory Map Toolkit
from .models import Point, Line, Polygon, Theme, Document, Image, AudioFile
from mmt_pages.models import Page
from mmt_api.serializers import PointSerializer, PolygonSerializer, PointDetailSerializer, DocumentSerializer
from .vector_tile_helpers import tileIsValid, tileToEnvelope, envelopeToBoundsSQL


def index(request):
	"""Base map"""

	themes = Theme.objects.all()
	pages = Page.objects.all().order_by('order')

	return render(request, 'mmt_map/index.html', {'themes': themes})


def feature_detail(request, pk, source_layer):
	"""Get info about a single feature"""

	if source_layer == 'points':
		feature = get_object_or_404(Point, id=pk)
		documents = Document.objects.filter(point=feature)
		images = Image.objects.filter(point=feature)
		audio = AudioFile.objects.filter(point=feature)
	elif source_layer == 'polygons':
		feature = get_object_or_404(Polygon, id=pk)
		documents = Document.objects.filter(polygon=feature)
		images = Image.objects.filter(polygon=feature)
		audio = AudioFile.objects.filter(polygon=feature)
	elif source_layer == 'lines':
		feature = get_object_or_404(Line, id=pk)
		documents = Document.objects.filter(line=feature)
		images = Image.objects.filter(line=feature)
		audio = AudioFile.objects.filter(line=feature)

	attachments_base = {'documents': documents, 'images': images, 'audio': audio}

	attachments = []
	for key, value in attachments_base.items():
		for v in value:
			attachments.append(v)
	
	attachments = sorted(attachments, key=lambda attachment: attachment.order)

	host = request.get_host()

	today = datetime.today()

	return render(request, 'mmt_map/feature.html', {'feature': feature, 'attachments': attachments, 'host': host, 'today': today })


def text_only_feature_list(request):
	"""A text only representation of features to provide access to memory map content for blind and partially-sighted users"""

	themes = Theme.objects.all()

	return render(request, 'mmt_map/feature_list.html', {'themes': themes})


# Vector tiles are optionally cached to stop the database being spammed to heavily.
@cache_page(60 * config.CACHE_TIMEOUT)
def vector_tile(request, z, x, y, tile_format):
	"""
	Returns a vector tile. Uses raw SQL because GeoDjango can't return vector tiles (though to my mind it should). Tiles are cached so as to make large maps more performant, at the expense of updates not being visible immediately.
	"""
	tile = {
		'zoom': int(z),
		'x': int(x),
		'y': int(y),
		'format': tile_format
	}

	if not tileIsValid(tile):
		return HttpResponse('tile not valid')

	env = tileToEnvelope(tile)
	env = envelopeToBoundsSQL(env)

	
	sql_tmpl = """
		WITH 
		bounds AS (
			SELECT {env} AS geom, 
				   {env}::box2d AS b2d
		),
		mvtgeom AS (
			SELECT ST_AsMVTGeom(ST_Transform(t.{geomColumn}, 3857), bounds.b2d) AS geom, 
				   {attrColumns}
			FROM {table} t, bounds
			WHERE ST_Intersects(t.{geomColumn}, ST_Transform(bounds.geom, {srid})) AND published = TRUE
		) 
		SELECT ST_AsMVT(mvtgeom.*, {layerName}) FROM mvtgeom
		"""

	# The layers have to be hard-coded because we're using SQL not the ORM. Must be changed if you update the models

	layers = {
		'points': {
			'table': 'mmt_map_point',
			'layerName': '\'points\''
		},
		'polygons': {
			'table': 'mmt_map_polygon',
			'layerName': '\'polygons\''
		},
		'lines': {
			'table': 'mmt_map_line',
			'layerName': '\'lines\''
		}
	}

	# Build the HttpResponse

	response = HttpResponse()
	response['Access-Control-Allow-Origin'] = '*'
	response['Content-type'] = 'application/vnd.mapbox-vector-tile'

	# Loop over the layers and concatenate them into the response

	for layer, attrs in layers.items():
		sql = sql_tmpl.format(env=env, attrColumns='id, name, weight, theme_id, tag_str', srid='4326', geomColumn='geom', table=attrs['table'], layerName=attrs['layerName'])

		with connection.cursor() as cursor:
			cursor.execute(sql)
			pbf = cursor.fetchone()[0]
	
		response.write(pbf.tobytes())
	
	# Return the tile

	return response


def tile_json(request):
	"""Returns a tileJSON object describing the vector tiles hosted in the Memory Map toolkit database."""
	
	scheme = request.scheme
	host = request.get_host()

	json = {
		'tileJSON': '2.2.0',
		'name': 'Memory Map Toolkit Interactive Features',
		'tiles': [
			scheme + '://' + host + '/tiles/{z}/{x}/{y}.pbf'
		],
	}

	return JsonResponse(json)

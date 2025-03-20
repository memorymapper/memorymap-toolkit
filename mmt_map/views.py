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
from psycopg2 import sql
import requests

# Third Party Django apps
from constance import config

# Memory Map Toolkit
from .models import Point, Line, Polygon, Theme, Document, Image, AudioFile, TagList, MapLayer
from mmt_pages.models import Page
from mmt_api.serializers import PointSerializer, PolygonSerializer, PointDetailSerializer, DocumentSerializer
from .vector_tile_helpers import tileIsValid, tileToEnvelope


def index(request):
	"""Base map"""

	themes = Theme.objects.all()
	pages = Page.objects.all().order_by('order')
	tag_lists = TagList.objects.filter(published=True).order_by('order')

	bounds = None
	
	if (config.BOUNDS_SW_LONGITUDE != 0.0) and (config.BOUNDS_SW_LATITUDE != 0.0) and (config.BOUNDS_NE_LATITUDE != 0.0) and (config.BOUNDS_NE_LONGITUDE != 0.0):

		bounds = [[config.BOUNDS_SW_LONGITUDE,config.BOUNDS_SW_LATITUDE],[config.BOUNDS_NE_LONGITUDE,config.BOUNDS_NE_LATITUDE]]


	return render(request, 'mmt_map/index.html', {'themes': themes, 'bounds': bounds, 'tag_lists': tag_lists})


def text_only_feature_list(request):
	"""A text only representation of features to provide access to memory map content for blind and partially-sighted users"""

	themes = Theme.objects.all()
	tag_lists = TagList.objects.filter(published=True).order_by('order')

	return render(request, 'mmt_map/feature_list.html', {'themes': themes, 'tag_lists': tag_lists})


# Vector tiles are optionally cached to stop the database being spammed too heavily.
@cache_page(60 * config.CACHE_TIMEOUT)
def vector_tile(request, z, x, y, tile_format):
	"""
	Returns a vector tile. Uses raw SQL because GeoDjango can't return vector tiles (though to my mind it should). Tiles are optionally cached so as to make large maps more performant, at the expense of updates not being visible immediately. Adapted from https://github.com/pramsey/minimal-mvt, though refactored so the query is built without using string.format()!
	"""
	tile = {
		'zoom': int(z),
		'x': int(x),
		'y': int(y),
		'format': tile_format
	}

	if not tileIsValid(tile):
		return HttpResponse('<p>Tile request not valid</p>', status=400)

	env = tileToEnvelope(tile)

	DENSIFY_FACTOR = 4
	env['segSize'] = (env['xmax'] - env['xmin'])/DENSIFY_FACTOR

	# The query has to be built manually to return the geometries as vector tiles. Must be changed if you update the models

	sql_tmpl = """
		WITH 
		"bounds" AS (
			SELECT ST_Segmentize(ST_MakeEnvelope(%(xmin)s, %(ymin)s, %(xmax)s, %(ymax)s, 3857),%(segSize)s) AS "geom", 
				   ST_Segmentize(ST_MakeEnvelope(%(xmin)s, %(ymin)s, %(xmax)s, %(ymax)s, 3857),%(segSize)s)::box2d AS "b2d"
		),
		"mvtgeom" AS (
			SELECT ST_AsMVTGeom(ST_Transform("t"."geom", 3857), "bounds"."b2d") AS "geom", 
				   "t"."id", "name", "weight", "theme_id", "tag_str", "thumbnail_url", "uuid",
				   "mmt_map_document"."slug", "attachments"
			FROM  {table} "t" 
				LEFT JOIN mmt_map_document
					ON mmt_map_document.point_id = "t".id,
			"bounds"
			WHERE ST_Intersects("t"."geom", ST_Transform("bounds"."geom", 4326)) AND "t"."published" = TRUE
		) 
		SELECT ST_AsMVT("mvtgeom".*, {layerName}) FROM "mvtgeom"
	"""

	# Map the geometry types to PostGIS database tables and layer names for consumption by MapboxGL

	layers = {
		'points': {
			'table': 'mmt_map_point',
			'layerName': "points"
		},
		'polygons': {
			'table': 'mmt_map_polygon',
			'layerName': "polygons"
		},
		'lines': {
			'table': 'mmt_map_line',
			'layerName': "lines"
		},
		'mulipoints': {
			'table': 'mmt_map_multipoint',
			'layerName': "multipoints"
		}
	}

	# Build the HttpResponse

	response = HttpResponse()
	response['Access-Control-Allow-Origin'] = '*'
	response['Content-type'] = 'application/vnd.mapbox-vector-tile'

	# Loop over the layers and concatenate them into the response

	for layer, attrs in layers.items():

		query = sql.SQL(sql_tmpl).format(table=sql.Identifier(attrs['table']), layerName=sql.Literal(attrs['layerName']))

		params = {'xmin': env['xmin'], 'ymin': env['ymin'], 'xmax': env['xmax'], 'ymax': env['ymax'], 'segSize': env['segSize']}

		with connection.cursor() as cursor:
			cursor.execute(query, params)
			pbf = cursor.fetchone()[0]
	
		response.write(pbf.tobytes())
	
	# Return the tile

	return response


def tile_json(request):
	"""Returns a tileJSON object describing the vector tiles hosted in the Memory Map toolkit database."""

	if request.is_secure():
		scheme = 'https'
	else:
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

def style_json(request):
	"""Returns the base map style for the main map for use in the admin site"""

	if request.is_secure():
		scheme = 'https'
	else:
		scheme = request.scheme

	host = request.get_host()

	# This works by getting the base map style, then appending the raster layers to the returned
	# styleJSON object

	maptiler_key = config.MAPTILER_KEY
	style_url = config.MAPTILER_STYLE

	params = {'key': maptiler_key}

	r = requests.get(style_url, params=params)

	if r.status_code == requests.codes.ok:
		style = r.json()

		sources = []
		layers = []

		for layer in MapLayer.objects.all():
			style['sources'][layer.slug] = {
				'type': 'raster',
				'url': layer.tilejson_url,
				'tileSize': 256
			}
			
			l = {
				'id': layer.slug,
				'type': 'raster',
				'source': layer.slug,
				'visibility': 'visible'
			}

			style['layers'].append(l)
		
		return JsonResponse(style)
	
	else:
		return JsonResponse({'ok': False})

	



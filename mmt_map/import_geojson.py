# Utility function to import GeoJSON data to memory mapper from an external URL
import requests
from .models import Point, Polygon, Line, Theme, Document, TagList, MultiPoint
from django.contrib.gis.geos import GEOSGeometry

def import_geojson(url, title, fallback, theme, props_to_tags):
    """
    Import geojson feature collection from an external URL. Saves the properties of feature
    to the 'body' field of the associated document.
    Param str url: the url of the GeoJSON feature collection
    Param str title: the geojson property to use for the title of the feature and its associated
    document 
    Param str fallback: a fallback string to use if the title prop is empty
    Param str theme: the title of the theme to add these features to
    Param dict props_to_tags: a dictionary of tag groups and props for features, in this format:
    {
        'Surname': 'surname',
        'Forename': 'forename'
    }
    
    """
    response = requests.get(url)
    data = response.json()

    if data['type'] != 'FeatureCollection':
        return 'Data is not a FeatureCollection' 
    
    # Create the TagLists, if necessary
    for key in props_to_tags.keys():
        TagList.objects.get_or_create(name=key, published=True)

    for f in data['features']:
        props = ''.join(['<li>{k}: {v}</li>'.format(k=key, v=str(value)) for key, value in f['properties'].items() if value])
        name = f['properties'][title]
        if not name:
            name = fallback
        t = Theme.objects.get_or_create(name=theme)
        geom = GEOSGeometry(str(f['geometry']))

        feature = None

        if f['geometry']['type'] in ['Polygon', 'MultiPolygon']:
            feature = Polygon.objects.create(name=name, theme=t[0], published=True, geom=geom)
            feature.save()
            Document.objects.create(title=name, polygon=feature, body='<ul>{props}</ul>'.format(props=props), published=True).save()
        elif f['geometry']['type'] in ['Point']:
            feature = Point.objects.create(name=name, theme=t[0], published=True, geom=geom)
            feature.save()
            Document.objects.create(title=name, point=feature, body='<p>{props}</p>'.format(props=props), published=True).save()
        elif f['geometry']['type'] in ['LineString', 'MultiLineString']:
            feature = Line.objects.create(name=name, theme=t[0], published=True, geom=geom)
            feature.save()
            Document.objects.create(title=name, line=feature, body='<p>{props}</p>'.format(props=props), published=True).save()
        elif f['geometry']['type'] in ['MultiPoint']:
            feature = MultiPoint.objects.create(name=name, theme=t[0], published=True, geom=geom)
            feature.save()
            Document.objects.create(title=name, multipoint=feature, body='<p>{props}</p>'.format(props=props), published=True).save()

        
        # Add the tags to the feature
        props = list(props_to_tags.values())
        tags = [value for key, value in f['properties'].items() if key in props]

        for t in tags:
            if t: # In case of null value
                feature.tags.add(t)

        feature.save()

        # Add the tags to the correct TagList
        # First, group them
        grouped_tags = {}

        for prop_name, value in f['properties'].items():
            group = [g for g, v in props_to_tags.items() if v == prop_name]
            if len(group):
                try:
                    grouped_tags[group[0]].append(value)
                except:
                    grouped_tags[group[0]] = [value]

        # Get the actual tag instances as a list
        feature_tags = feature.tags.all()

        # Then iterate over them, adding them to the correct TagList object
        for ft in feature_tags:
            for group, tags in grouped_tags.items():
                if ft.name in tags:
                    tl = TagList.objects.get(name=group)
                    tl.tags.add(ft)
                    tl.save()

    return 'Geometry Loaded'


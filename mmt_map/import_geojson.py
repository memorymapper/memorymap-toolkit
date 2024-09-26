# Utility function to import GeoJSON data to memory mapper from an external URL
import requests
from .models import Point, Polygon, Line, Theme, Document, TagList, MultiPoint
from django.contrib.gis.geos import GEOSGeometry
from django.utils.html import urlize
from django.core import files
from io import BytesIO


def import_geojson(url, feature_title, doc_title, fallback, theme, props_to_tags=None, doc_fields=[], url_field=None, popup_image_field=None):
    """
    Import geojson feature collection from an external URL. Saves the properties of feature
    to the 'body' field of the associated document.
    Param str url: the url of the GeoJSON feature collection
    Param str feature_title: the geojson property to use for the title of the feature
    Param str doc_title: the title to use for the associated document
    Param str fallback: a fallback string to use if the title prop is empty
    Param str theme: the column to use to sort these features into themes
    Param dict props_to_tags: a dictionary of tag groups and props for features, in this format:
    {
        'Surname': 'surname',
        'Forename': 'forename'
    }
    Param list doc_field: the properties from which to populate the document. If left blank defaults to the properties attached to the feature.
    Param str url_field: if any of the properties of the GeoJSON properties are a URL, name it here so that it can be turned into a proper hyperlink
    Param str popup_image_field: a property containing a url of an image file to be set as the popup_image
    """
    response = requests.get(url)
    data = response.json()

    if data['type'] != 'FeatureCollection':
        return 'Data is not a FeatureCollection' 
    
    # Create the TagLists, if necessary
    if props_to_tags:
        for key in props_to_tags.keys():
            TagList.objects.get_or_create(name=key, published=True)

    for f in data['features']:

        try:
            geom = GEOSGeometry(str(f['geometry']))
        except Exception as err:
            print(err)
            continue

        # If there aren't any coordinates, don't add the record...
        if len(geom.coords) == 0:
            print('No geometry')
            continue

        if len(doc_fields) == 0:
            body = ''.join(['<p><strong>{k}</strong>: {v}</p>'.format(k=key, v=str(value)) for key, value in f['properties'].items() if value])
        
        else:
            if url_field:
                f['properties'][url_field] = urlize(f['properties'][url_field])
            body = ''.join(['<p><strong>{k}</strong>: {v}</p>'.format(k=key, v=str(value)) for key, value in f['properties'].items() if value and key in doc_fields])

        try:
            name = f['properties'][feature_title][0:127] # trim to fit in
        except:
            name = None
        
        if not name:
            name = fallback
        
        t = Theme.objects.get_or_create(name=f['properties'][theme].strip())
        
        feature = None

        if f['geometry']['type'] in ['Polygon', 'MultiPolygon']:
            feature = Polygon.objects.create(name=name, theme=t[0], published=True, geom=geom)
            feature.save()
            Document.objects.create(title=doc_title, polygon=feature, body=body, published=True).save()

        elif f['geometry']['type'] in ['Point']:
            feature = Point.objects.create(name=name, theme=t[0], published=True, geom=geom)
            feature.save()
            Document.objects.create(title=doc_title, point=feature, body=body, published=True).save()

        elif f['geometry']['type'] in ['LineString', 'MultiLineString']:
            feature = Line.objects.create(name=name, theme=t[0], published=True, geom=geom)
            feature.save()
            Document.objects.create(title=doc_title, line=feature, body=body, published=True).save()

        elif f['geometry']['type'] in ['MultiPoint']:
            feature = MultiPoint.objects.create(name=name, theme=t[0], published=True, geom=geom)
            feature.save()
            Document.objects.create(title=doc_title, multipoint=feature, body=body, published=True).save()

        # If there's an image file url, process it...

        if popup_image_field:
            url = f['properties'][popup_image_field]
            file_name = url.split("/")[-1]
            r = requests.get(f['properties'][popup_image_field])
            if r.status_code == 200:
                fp = BytesIO()
                fp.write(r.content)

                try:
                    feature.popup_image.save(file_name, files.File(fp))
                    feature.save()
                except Exception as err:
                    print(err)
                    continue

        if not props_to_tags:
            continue
        
        # Add the tags to the feature
        props = list(props_to_tags.values())
        tags = [value.strip() for key, value in f['properties'].items() if key in props]

        for t in tags:
            if t: # In case of null value
                feature.tags.add(t[0:99])

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


from django.conf import settings

def site_settings(request):
    site_title = settings.SITE_TITLE
    map_center = settings.MAP_CENTER

    base_map_style = settings.BASE_MAP_STYLE
    base_map_source = settings.BASE_MAP_SOURCE

    zoom = settings.ZOOM
    min_zoom = settings.MIN_ZOOM
    max_zoom = settings.MAX_ZOOM
    max_bounds = settings.MAX_BOUNDS
    scale = settings.SCALE

    pitch = settings.PITCH
    bearing = settings.BEARING

    welcome_message = settings.WELCOME_MESSAGE

    metadata = settings.SITE_METADATA

    return {'site_title': site_title, 'map_center': map_center, 'base_map_source': base_map_source, 'zoom': zoom, 'min_zoom': min_zoom, 'max_zoom': max_zoom, 'welcome_message': welcome_message, 'metadata': metadata, 'max_bounds': max_bounds, 'scale': scale, 'base_map_style': base_map_style, 'pitch': pitch, 'bearing': bearing}
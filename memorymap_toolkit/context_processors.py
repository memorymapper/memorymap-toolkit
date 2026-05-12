# Django Core
from django.conf import settings

# Third Party Django apps
from constance import config

# Local
from .utils import ensure_maptiler_key


def site_settings(request):
    # Create a modified config object that includes the processed BASE_MAP_STYLE_URL
    config_dict = {
        'BASE_MAP_STYLE_URL': ensure_maptiler_key(config.BASE_MAP_STYLE_URL, config.MAPTILER_KEY)
    }
    
    return {
        'config': config,
        'config_base_map_style_url': config_dict['BASE_MAP_STYLE_URL']
    }

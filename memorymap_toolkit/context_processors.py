# Django Core
from django.conf import settings

# Third Party Django apps
from constance import config


def site_settings(request):
    return {'config': config}
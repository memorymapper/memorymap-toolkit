from django.conf import settings
from constance import config

class MediaURLMiddleware:
    """
    Ensures that the MEDIA_URL setting in constance is used for uploading media files. This needs to be dynamically configurable
    as Memory Mapper has multiple instances and it's necessary to allow users to set this if they're using the next.js frontend.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        settings.MEDIA_URL = config.MEDIA_URL

        return response
        
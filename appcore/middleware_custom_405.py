from django.http import HttpResponseNotAllowed
from django.template import RequestContext
from django.template import loader

from config import settings


class ExceptionMiddleware405(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if isinstance(response, HttpResponseNotAllowed) and not settings.DEBUG:
            context = RequestContext(request)
            response.content = loader.render_to_string("405.html", context=locals())
        return response

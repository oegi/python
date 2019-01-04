import os

from django.http import HttpResponse, Http404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


class ExportView(View):
    http_method_names = ['get', ]

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ExportView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        datag = request.GET
        filename = datag.get('file_name')
        directory = datag.get('directory')

        file_path = os.path.join('/{}/'.format(directory), filename)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh, content_type='application/ms-excel')
                response['Content-Disposition'] = 'inline; filename={}'.format(filename)
                return response
        raise Http404

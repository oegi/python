import os
import time

from django.db.models import F
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View

from appcore.helpers.binnacle import BinnacleHelper
from appcore.models import Questions
from appcore.models import Sockets, Binnacle
from appcore.models import SocketsMeasure


class BinnacleView(TemplateView):
    template_name = 'binnacle.html'

    def get(self, request, *args, **kwargs):
        questions = Questions.objects.filter(category__title='BITACORA', is_active=True, )
        binnacles = Binnacle.objects.distinct().values('period_rescue').order_by('-period_rescue')
        binnacles_pends = Binnacle.objects.filter(state='PENDIENTE')

        origin = Sockets.objects.filter(user_defined01__isnull=False, description='Real') \
            .exclude(user_defined01='').distinct().values('user_defined01') \
            .order_by('user_defined01')

        state = SocketsMeasure.objects.filter(idsocket__isnull=False, description='Real') \
            .exclude(idsocket='').distinct().values('idsocket').order_by('idsocket')
        return render(request, self.template_name, locals())


class ExportView(View):
    http_method_names = ['get', ]

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ExportView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        binnacles = Binnacle.objects.all().values(
            'cod_binnacle',
            'noins',
            'idsocket',
            'date_start',
            'date_end',
            'date_rescue',
            'origin',
            'state',
            'user_defined01',
            'user_defined03',
            'user_defined02',
            'idclient',
            'user',
            'mante_num',
            'comments',
            descrip_reason=F('reason__description'),
        )
        binnacle_helper = BinnacleHelper(
            detail=binnacles,
        )
        binnacle_helper.save()
        response = self.download(
            '/BITACORA/Bitacora.xlsx',
            filename='Bitacora_' + time.strftime("%d/%m/%y")
        )
        response.set_cookie('binnacle_response', 'success')
        return response

    @staticmethod
    def download(path, filename):
        file_path = os.path.join(path)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh, content_type='application/ms-excel')
                response['Content-Disposition'] = 'inline; filename={}.xlsx'.format(filename)
                return response
        raise Http404

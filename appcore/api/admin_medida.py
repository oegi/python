import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import View

from appcore.models import Sockets, SocketsMeasure


class MeasurementView(View):
    http_method_names = ['post']

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        id_client = [data.get('idclient', None)]
        substation = data.get('substation', None)

        if '__all__' in id_client:
            id_client = Sockets.objects.filter(
                idclient__isnull=False,
                description='Real'
            ).distinct().values('idclient').order_by('idclient')
            id_client = [x.get('idclient') for x in id_client]

        sockets_measure = SocketsMeasure.objects.filter(
            idclient__in=id_client,
            idclient__isnull=False,
            user_defined01__in=substation.split(','),
            user_defined01__isnull=False,
            description='Real'
        ).exclude(user_defined01=None) \
            .values('idsocket', 'is_active')

        return HttpResponse(json.dumps(
            dict(data=list(sockets_measure))
        ), content_type='application/json')

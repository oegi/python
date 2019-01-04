import json

from django.db.models import Count, CASCADE
from django.db.models.fields.related import ForeignObject
from django.db.models.options import Options
from django.db.models.sql.datastructures import Join
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import View

from appcore.models import Sockets, SocketHide, SocketChannel


class SubstationView(View):
    http_method_names = ['post']

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        socket_hide = SocketHide.objects.values('idsocket')
        socket_hide = [x.get('idsocket') for x in socket_hide]

        id_client = [data.get('idclient', None)]

        if '__all__' in id_client:
            id_client = Sockets.objects.filter(idclient__isnull=False, description='Real') \
                .exclude(idsocket__in=socket_hide).distinct().values('idclient').order_by('idclient')

        substations = Sockets.objects.filter(idclient__in=id_client, idclient__isnull=False, description='Real') \
            .exclude(user_defined01=None).exclude(idsocket__in=socket_hide) \
            .values('user_defined01').annotate(dcount=Count('user_defined01'))

        return HttpResponse(json.dumps(
            dict(data=list(substations))
        ), content_type='application/json')


class LevelTensionsView(View):
    http_method_names = ['post']

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        socket_hide = SocketHide.objects.values('idsocket')
        socket_hide = [x.get('idsocket') for x in socket_hide]

        id_client = [data.get('idclient', None)]
        if '__all__' in id_client:
            id_client = Sockets.objects.filter(
                idclient__isnull=False,
                description='Real'
            ).exclude(idsocket__in=socket_hide).distinct().values('idclient').order_by('idclient')

        user_defined01 = data.get('user_defined01', None)

        select_extra = {
            'user_defined03': "CONVERT(INT, user_defined03)"
        }

        level_tensions = Sockets.objects.filter(
            idclient__in=id_client,
            idclient__isnull=False,
            user_defined01__in=user_defined01,
            user_defined01__isnull=False,
            description='Real'
        ).exclude(user_defined03='').exclude(idsocket__in=socket_hide).distinct() \
            .extra(select=select_extra).values('user_defined03').order_by('user_defined03')

        return HttpResponse(json.dumps(
            dict(data=list(level_tensions))
        ), content_type='application/json')


class MeasurementPointsView(View):
    http_method_names = ['post']

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        socket_hide = SocketHide.objects.values('idsocket')
        socket_hide = [x.get('idsocket') for x in socket_hide]
        id_client = [data.get('idclient', None)]
        if '__all__' in id_client:
            id_client = Sockets.objects.filter(
                idclient__isnull=False,
                description='Real'
            ).exclude(idsocket__in=socket_hide).distinct().values('idclient').order_by('idclient')

        user_defined01 = data.get('user_defined01', None)
        user_defined03 = data.get('user_defined03', None)

        idsocket = Sockets.objects.filter(
            idclient__in=id_client,
            idclient__isnull=False,
            user_defined01__in=user_defined01,
            user_defined01__isnull=False,
            user_defined03__in=user_defined03,
            user_defined03__isnull=False,
            description='Real'
        ).exclude(idsocket='').exclude(idsocket__in=socket_hide).distinct() \
            .values('idsocket').order_by('idsocket')

        return HttpResponse(json.dumps(
            dict(data=list(idsocket))
        ), content_type='application/json')


class MeasurementSocketView(View):
    http_method_names = ['post']

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        idclient = data.get('idclient')

        select_extra = {
            'last_date': "FORMAT(DATEADD(mi, 15, max_datetime), 'dd-MM-yyyy HH:mm', 'es-CL' )"
        }

        sockets = Sockets.objects.filter(
            idclient=idclient,
            idclient__isnull=False,
            description='Real'
        ).extra(select=select_extra).exclude(idsocket='') \
            .distinct() \
            .values('id_soc', 'idsocket', 'noins', 'last_date').order_by('noins')

        _join_obj = ForeignObject(
            to=SocketChannel,
            on_delete=CASCADE,
            from_fields=[None],
            to_fields=[None],
            rel=None,
            related_name=None
        )

        _join_obj.opts = Options(Sockets._meta)
        _join_obj.opts.model = Sockets
        _join_obj.get_joining_columns = lambda: (('ID_SOC', 'id_soc',),)

        _join = Join(SocketChannel._meta.db_table, Sockets._meta.db_table, 'SCH', 'INNER JOIN', _join_obj, True)
        sockets.query.join(_join)

        return HttpResponse(json.dumps(
            dict(data=list(sockets))
        ), content_type='application/json')

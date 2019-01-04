# -*- coding: utf-8 -*-
import os
import uuid
from collections import defaultdict
from datetime import datetime

from django.contrib import messages
from django.db.models import Count, Max
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.generic.base import View

from appcore.helpers.date import back_months
from appcore.helpers.exceptions import ErrorException
from appcore.helpers.register import RegisterHelper, RegisterCSVHelper
from appcore.models import (
    MeasureHead,
    MeasureDetail,
    MeasureDetailHo,
    Parameter,
    SocketHide)
from appcore.models import Questions
from appcore.models import Sockets, ChannelConfig


class IndexView(TemplateView):
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):

        quantity_points_db = 200
        try:
            parameter = Parameter.objects.get(name='QT_MEASU_POINTS')
            quantity_points_db = int(parameter.value)
        except Parameter.DoesNotExist:
            pass

        socket_hide = SocketHide.objects.values('idsocket')
        socket_hide = [x.get('idsocket') for x in socket_hide]

        questions = Questions.objects.filter(
            category__title='REGISTRO DESDE PLATAFORMA DE MEDIDAS (PRMTE)',
            is_active=True,
        )

        clients = Sockets.objects.filter(
            idclient__isnull=False,
            description='Real'
        ).exclude(idsocket__in=socket_hide).distinct().values('idclient').order_by('idclient')

        substations = Sockets.objects.filter(
            user_defined01__isnull=False,
            description='Real'
        ).exclude(user_defined01='').exclude(idsocket__in=socket_hide).values('user_defined01').annotate(
            dcount=Count('user_defined01')
        )

        select_extra = {
            'user_defined03': "CONVERT(INT, user_defined03)"
        }

        level_tensions = Sockets.objects.filter(
            user_defined03__isnull=False,
            description='Real'
        ).exclude(user_defined03='').exclude(idsocket__in=socket_hide) \
            .distinct().extra(select=select_extra).values('user_defined03').order_by('user_defined03')

        measurement_points = Sockets.objects.filter(
            idsocket__isnull=False,
            description='Real'
        ).exclude(idsocket='').exclude(idsocket__in=socket_hide) \
            .distinct().values('idsocket').order_by('idsocket')

        months = back_months(datetime.now(), 4)

        return render(request, self.template_name, locals())


class ExportView(View):
    http_method_names = ['post', ]

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ExportView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = request.POST
        massive_point = data.get('massive_point', None)

        if massive_point != 'MASSIVE_POINT':
            points_cn = data.get('points_cn', None)
            client = [data.get('client', None)]
            socket_hide = SocketHide.objects.values('idsocket')
            socket_hide = [x.get('idsocket') for x in socket_hide]
            quantity_points_db = 200
            try:
                parameter = Parameter.objects.get(name='QT_MEASU_POINTS')
                quantity_points_db = int(parameter.value)
            except Parameter.DoesNotExist:
                pass
            if int(points_cn) > quantity_points_db:
                messages.error(request, 'Ha Superado el limite de puntos de medidas permitido (%s). '
                                        'Por favor ajuste los filtros o descargue todos los puntos '
                                        'de medida asociado a un coordinado.' % quantity_points_db)
                return redirect('path_register')

            substation = data.get('substation_hidden', None)
            substation = (substation != '') and substation.split(',') or None
            level_tension = data.get('level_tension_hidden', None)
            level_tension = (level_tension != '') and level_tension.split(',') or None
            idsocket = data.get('measurement_point_hidden', None)
            idsocket = (idsocket != '') and idsocket.split(',') or None

            if '__all__' in client:
                client = Sockets.objects.filter(description='Real') \
                    .exclude(idsocket__in=socket_hide).distinct().values('idclient').order_by('idclient')
                client = [x.get('idclient') for x in client]

            if substation is None:
                substation = Sockets.objects.filter(idclient__in=client, description='Real') \
                    .exclude(idsocket__in=socket_hide).values('user_defined01').annotate(dcount=Count('user_defined01'))
                substation = [x.get('user_defined01') for x in substation]

            if level_tension is None:
                level_tension = Sockets.objects.filter(user_defined01__in=substation, description='Real') \
                    .exclude(idsocket__in=socket_hide).distinct().values('user_defined03').order_by('user_defined03')
                level_tension = [x.get('user_defined03') for x in level_tension]

            if idsocket is None:
                idsocket = Sockets.objects \
                    .filter(user_defined01__in=substation, user_defined03__in=level_tension, description='Real') \
                    .exclude(idsocket__in=socket_hide).distinct().values('idsocket').order_by('idsocket')
                idsocket = [x.get('idsocket') for x in idsocket]

            type_file = data.get('type_file', None)
            month, year = data.get('months', []).split('|')
            hr_or_min = data.get('hr_or_min', None)
            datetime_ce = '{}{}'.format(year, month)
            name_output = 'MEDIDAS_PRMT_{}_'.format(datetime_ce)
            if data.get('client', None) != '__all__':
                name_output = '{}_{}'.format(str(data.get('client', None)).upper(), datetime_ce)

            if len(substation) == 1:
                name_output = '{}_{}'.format(str(substation[0]).upper(), datetime_ce)

            if len(level_tension) == 1:
                name_output = '{}_{}'.format(str(level_tension[0]).upper(), datetime_ce)

            if len(idsocket) == 1:
                name_output = '{}_{}'.format(str(idsocket[0]).upper(), datetime_ce)

            name_output_m = 'MEDIDAS_PRMT_{}'
            if data.get('client', None) != '__all__':
                name_output_m = '{}_{}'.format(str(data.get('client', None)).upper(), '{}')

            if data.get('client', None) != '__all__' and len(substation) == 1:
                file_str_output = '{}_{}'.format(str(data.get('client', None)).upper(), str(substation[0]).upper(), )
                name_output = '{}_{}'.format(file_str_output, datetime_ce)

            if len(substation) == 1 and len(level_tension) == 1:
                file_str_output = '{}_{}'.format(str(substation[0]).upper(), str(level_tension[0]).upper(), )
                name_output = '{}_{}'.format(name_output_m.format(file_str_output), datetime_ce)

            if len(substation) == 1 and len(idsocket) == 1:
                file_str_output = '{}_{}'.format(str(substation[0]).upper(), str(idsocket[0]).upper(), )
                name_output = '{}_{}'.format(name_output_m.format(file_str_output), datetime_ce)

            if len(level_tension) == 1 and len(idsocket) == 1:
                file_str_output = '{}_{}'.format(str(level_tension[0]).upper(), str(idsocket[0]).upper(), )
                name_output = '{}_{}'.format(name_output_m.format(file_str_output), datetime_ce)

            if len(substation) == 1 and len(level_tension) == 1 and len(idsocket) == 1:
                substation_output = str(substation[0]).upper()
                level_tension_output = str(level_tension[0]).upper()
                idsocket_output = str(idsocket[0]).upper()
                file_str_output = '{}_{}_{}'.format(substation_output, level_tension_output, idsocket_output, )
                name_output = '{}_{}'.format(name_output_m.format(file_str_output), datetime_ce)

            channels = ChannelConfig.objects.filter(report_field=1).values().order_by('report_order_field')

            if year != 0:
                year = (9 < int(year)) and year or '0' + month

            if month != 0:
                month = (9 < int(month)) and month or '0' + month

            select_extra = {
                'binnacles_des': "SELECT b.binnacle FROM binnacle_period b WHERE b.id_soc =  "
                                 "[measure_head].[ID_SOC] AND b.is_backup = [measure_head].[is_backup] "
                                 "AND b.period_rescue = %s" % int(year + month)
            }

            measure_head = MeasureHead.objects.filter(
                idclient__in=client,
                idsocket__in=idsocket,
                user_defined01__in=substation,
                user_defined03__in=level_tension,
                period_rescue=int(year + month)
            ).exclude(idsocket__in=socket_hide).extra(select_extra).order_by(
                'id_soc',
                'is_backup',
                'user_defined01',
                'idclient',
            ).values()

            id_soc_in = [x.get('id_soc') for x in measure_head]
            measure_detail = []
            measure_detail_cn = 0
            if hr_or_min == '1H':
                measure_detail_q = MeasureDetailHo.objects.filter(
                    id_soc__in=id_soc_in,
                    monthx=month,
                    yearx=year
                )
                measure_detail = measure_detail_q.order_by(
                    'id_soc',
                    'is_backup',
                    'yearx',
                    'monthx',
                    'dayx',
                    'hourx'
                ).values()

                try:
                    measure_detail_cn = measure_detail_q.values('id_soc').annotate(dcount=Count('id_soc')).aggregate(
                        Max('dcount')).get('dcount__max')
                except ErrorException:
                    pass

            if hr_or_min == '15MIN':
                measure_detail_q = MeasureDetail.objects.filter(
                    id_soc__in=id_soc_in,
                    monthx=month,
                    yearx=year
                )
                measure_detail = measure_detail_q.order_by(
                    'id_soc',
                    'is_backup',
                    'yearx',
                    'monthx',
                    'dayx',
                    'hourx',
                    'minute',
                    'minute_end'
                ).values()
                try:
                    measure_detail_cn = measure_detail_q.values('id_soc').annotate(dcount=Count('id_soc')).aggregate(
                        Max('dcount')).get('dcount__max')
                except ErrorException:
                    pass

            if len(measure_detail) == 0:
                messages.error(request, 'El filtro seleccionado no tiene datos')
                return redirect('path_register')

            details = defaultdict(lambda: defaultdict(list))
            if len(measure_detail) != 0:
                for x in measure_detail:
                    details[x.get('id_soc')][x.get('is_backup')].append(x)
            response = HttpResponse(content_type='text/csv')

            if type_file == 'csv':
                delimiter_db = ';'
                try:
                    parameter = Parameter.objects.get(name='DELIMITER_CSV')
                    delimiter_db = parameter.value
                except Parameter.DoesNotExist:
                    pass
                file_name = '{}.csv'.format(name_output)
                content = "attachment; filename = {0}".format(file_name)
                response['Content-Disposition'] = content
                register_csv_helper = RegisterCSVHelper(
                    head=measure_head,
                    detail=details,
                    channels=channels,
                    hr_or_min=hr_or_min,
                )

                register_csv_helper.save(response=response, delimiter=delimiter_db)
            if type_file == 'xlsx':
                sheet_name = name_output[:30]
                register_helper = RegisterHelper(
                    head=measure_head,
                    detail=details,
                    detail_cn=int(measure_detail_cn / len(set([x.get('is_backup') for x in measure_head]))),
                    channels=channels,
                    hr_or_min=hr_or_min,
                    sheet_name=sheet_name
                )
                path_uuid = '/tmp/{}.xlsx'.format(uuid.uuid1())
                register_helper.save(output=path_uuid, )
                response = self.download(
                    path_uuid,
                    filename=name_output
                )
        else:
            client = data.get('client', None)
            month, year = data.get('months', []).split('|')
            datetime_ce = '{}{}'.format(year, month)

            name_output = '{}_{}'.format(client, datetime_ce)

            if year != 0:
                year = (9 < int(year)) and year or '0' + month

            if month != 0:
                month = (9 < int(month)) and month or '0' + month

            directory_db = 'MEDIDAS_TOP'
            try:
                parameter = Parameter.objects.get(name='DIRECTORY_MEASU_TOP')
                directory_db = parameter.value
            except Parameter.DoesNotExist:
                pass

            directory_base = '/{}/{}/{}'.format(directory_db, year, month)
            path = '{}/{}.xlsx'.format(directory_base, name_output)

            if not os.path.exists(path):
                messages.error(request, 'No se encontró el archivo %s.xlsx en el siguiente '
                                        'directorio %s' % (name_output, directory_base))
                return redirect('path_register')

            response = self.download(
                path=path,
                filename=name_output
            )

        response.set_cookie('register_response', 'success')
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

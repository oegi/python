import json
import locale
from collections import defaultdict
from datetime import datetime, timedelta

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import View

from appcore.helpers import status
from appcore.helpers.exceptions import ErrorException
from appcore.models import ChannelOrder, MeasureDetail
from appcore.utils import datetime_range


class CollectorManualView(View):
    http_method_names = ['post', ]

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):
        data = request.body

        data_json = dict(data=None)
        http_response = dict(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

        try:
            data = json.loads(data)
        except ErrorException:
            data = None

        if data is not None:
            date_start = data.get('date_last')
            date_end = data.get('date_end')
            interval = data.get('interval')
            id_soc = data.get('id_soc')

            if date_start is not None and date_start is not '':
                date_start = datetime.strptime(date_start, '%d-%m-%Y %H:%M')

            if date_end is not None and date_end is not '':
                date_end = datetime.strptime(date_end, '%d-%m-%Y %H:%M')

            if isinstance(interval, str):
                interval = int(interval)

            columns = [{
                'title': 'Intervalos',
                'data': 'datetime'
            }]

            fields = ['id_soc', 'datetime']

            try:
                channel_order = ChannelOrder.objects.get(id_soc=id_soc)

                channel1 = channel_order.channel1
                if channel1 is not None and channel1 is not '':
                    columns.append({
                        'title': channel1,
                        'data': 'channel_val1',
                    })
                    fields.append('channel_val1')

                channel2 = channel_order.channel2
                if channel2 is not None and channel2 is not '':
                    columns.append({
                        'title': channel2,
                        'data': 'channel_val2',
                    })
                    fields.append('channel_val2')

                channel3 = channel_order.channel3
                if channel3 is not None and channel3 is not '':
                    columns.append({
                        'title': channel3,
                        'data': 'channel_val3',
                    })
                    fields.append('channel_val3')

                channel4 = channel_order.channel4
                if channel4 is not None and channel4 is not '':
                    columns.append({
                        'title': channel4,
                        'data': 'channel_val4',
                    })
                    fields.append('channel_val4')

                channel5 = channel_order.channel5
                if channel5 is not None and channel5 is not '':
                    columns.append({
                        'title': channel5,
                        'data': 'channel_val5',
                    })
                    fields.append('channel_val5')

                channel6 = channel_order.channel6
                if channel6 is not None and channel6 is not '':
                    columns.append({
                        'title': channel6,
                        'data': 'channel_val6',
                    })
                    fields.append('channel_val6')

                channel7 = channel_order.channel7
                if channel7 is not None and channel7 is not '':
                    columns.append({
                        'title': channel7,
                        'data': 'channel_val7',
                    })
                    fields.append('channel_val7')

                channel8 = channel_order.channel8
                if channel8 is not None and channel8 is not '':
                    columns.append({
                        'title': channel8,
                        'data': 'channel_val8',
                    })
                    fields.append('channel_val8')

                channel9 = channel_order.channel9
                if channel9 is not None and channel9 is not '':
                    columns.append({
                        'title': channel9,
                        'data': 'channel_val9',
                    })
                    fields.append('channel_val9')

                channel10 = channel_order.channel10
                if channel10 is not None and channel10 is not '':
                    columns.append({
                        'title': channel10,
                        'data': 'channel_val10',
                    })
                    fields.append('channel_val10')

                channel11 = channel_order.channel11
                if channel11 is not None and channel11 is not '':
                    columns.append({
                        'title': channel11,
                        'data': 'channel_val11',
                    })
                    fields.append('channel_val11')

                channel12 = channel_order.channel12
                if channel12 is not None and channel12 is not '':
                    columns.append({
                        'title': channel12,
                        'data': 'channel_val12',
                    })
                    fields.append('channel_val12')
            except ChannelOrder.DoesNotExist:
                pass

            date_subtract = date_start - timedelta(minutes=15 * interval)

            data_dt = defaultdict(dict)

            measure_detail = MeasureDetail.objects.filter(
                id_soc=id_soc,
                datetime__range=[date_subtract, date_start],
            ).values(*fields).order_by('id_soc')

            locale.setlocale(locale.LC_ALL, 'es_CL.utf-8')

            inc = 0
            if measure_detail.count() != 0:
                for k, m in enumerate(measure_detail):
                    for field in list(m):
                        value = m.get(field)
                        if value is None:
                            value = ''
                        if isinstance(value, datetime):
                            value = value.__format__('%d-%m-%Y %H:%M')

                        if field.__contains__('channel_'):
                            value = locale.format_string('%.2f', value, grouping=True)

                        data_dt[k].update({
                            'inc': k,
                            'class_secondary': 'dt-blue-grey',
                            'class': 'grey lighten-4 inp-decorate',
                            'attr': '',
                            'readonly': 'readonly',
                            field: value,
                        })
                    inc = k

            datetime_delta = datetime_range(start=date_start, end=date_end, delta=timedelta(minutes=15))

            inc = inc + 1
            for dd in datetime_delta:
                if date_start != dd:
                    for k, field in enumerate(fields):
                        value = ''
                        if k == 0:
                            value = id_soc
                        if k == 1 and isinstance(dd, datetime):
                            value = dd.__format__('%d-%m-%Y %H:%M')
                        data_dt[inc].update({
                            'inc': inc,
                            'class_secondary': 'dt-orange-grey',
                            'class': 'lighten-4 inp-decorate',
                            'attr': '',
                            'readonly': '',
                            field: value
                        })
                    inc += 1

            data_json = dict(data=[data_dt[k] for k in data_dt], columns=columns)
            http_response = dict(status=status.HTTP_200_OK, content_type='application/json')

        return HttpResponse(json.dumps(data_json), **http_response)

import os
import sys
from collections import defaultdict
import time

import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

# los modelo deben ir despeus del django.setup()
from appcore.models import MeasureHead, Sockets, SocketHide, MeasureDetail, ChannelConfig
from django.db.models import Count, Max
from appcore.helpers.register import RegisterHelper

hr_or_min = "15MIN"
datetime_ce = '201811'
month = '11'
year = '2018'

directory = os.path.join('/MEDIDAS_TOP/', year, month)

if not os.path.exists(directory):
    os.makedirs(directory)

# puntos de medidas ocultos y pasado a lista
socket_hide = SocketHide.objects.values('idsocket')
socket_hide = [x.get('idsocket') for x in socket_hide]

# Lista de clientes distintos
all_clients = Sockets.objects.exclude(user_defined03='').values_list('idclient', flat=True).distinct().order_by(
    'idclient')

# canales
channels = ChannelConfig.objects.filter(report_field=1).values().order_by('report_order_field')
channel_quantity = channels.count()

print("*** Generacion de medidas top PERIODO:" + str(datetime_ce))
for client_id in all_clients:
    try:
        print('------------------------------------------------------------------------------------')
        start = time.time()
        print(client_id)
        sheet_name = client_id[:30]

        name_file = sheet_name + "_" + datetime_ce + "." + "xlsx"

        full_path_excel = os.path.join(directory, name_file)
        print("full_path_excel:" + str(full_path_excel))

        select_extra = {
            'binnacles_des': "SELECT b.binnacle FROM binnacle_period b WHERE b.id_soc =  "
                             "[measure_head].[ID_SOC] AND b.is_backup = [measure_head].[is_backup] "
                             "AND b.period_rescue = %s" % int(year + month)
        }
        measure_head = MeasureHead.objects.filter(
            idclient=client_id,
            period_rescue=int(year + month),
        ).exclude(idsocket__in=socket_hide).extra(select_extra).order_by(
            'id_soc',
            'is_backup',
            'user_defined01',
            'idclient',
        ).values()

        id_soc_in = [x.get('id_soc') for x in measure_head]
        measure_detail = []
        measure_detail_cn = 0

        print("Total de socktets:" + str(len(id_soc_in)))

        if len(id_soc_in) > 0:

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
            except Exception as error:
                print("error: " + str(error))

            if len(measure_detail) >= 0:
                print('El filtro seleccionado no tiene datos')
                # return

                details = defaultdict(lambda: defaultdict(list))
                if len(measure_detail) != 0:
                    for x in measure_detail:
                        details[x.get('id_soc')][x.get('is_backup')].append(x)

                done = time.time()
                elapsed = done - start
                print("Tiempo Pre-Generacion:" + str(elapsed))
                register_helper = RegisterHelper(
                    head=measure_head,
                    detail=details,
                    detail_cn=int(measure_detail_cn / len(set([x.get('is_backup') for x in measure_head]))),
                    channels=channels,
                    hr_or_min=hr_or_min,
                    sheet_name=sheet_name
                )

                register_helper.save(output=full_path_excel, )
                done = time.time()
                elapsed = done - start
                print("Tiempo Generacion:" + str(elapsed))
            else:
                print("Error: Cliente sin cabezera")
        else:
            print("Error: Cliente sin sockets")

    except Exception as error:
        print("error:" + str(error))

import os
import sys
import time
from collections import defaultdict

import django
from django.db.models import Q

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

# los modelo deben ir despeus del django.setup()
from appcore.models import MeasureHead, Sockets, SocketHide, MeasureDetail, ChannelConfig
from django.db.models import Count, Max
from appcore.helpers.register import RegisterHelper

hr_or_min = "15MIN"

datetime_ce = time.strftime("%Y%m")
month = time.strftime("%m")  # '11'
year = time.strftime("%Y")  # '2018''

directory = os.path.join('/MEDIDAS_TOP/', year, month)

if not os.path.exists(directory):
    os.makedirs(directory)




def substations(all_substation, channels):
    print("Total de Substation:" + str(len(all_substation)))
    print("*** Generacion de medidas top PERIODO:" + str(datetime_ce))
    try:
        start = time.time()
        full_path_excel = os.path.join(directory, name_file)
        print("full_path_excel:" + str(full_path_excel))

        select_extra = {
            'binnacles_des': "SELECT b.binnacle FROM binnacle_period b WHERE b.id_soc =  "
                             "[measure_head].[ID_SOC] AND b.is_backup = [measure_head].[is_backup] "
                             "AND b.period_rescue = %s" % int(year + month)
        }
        measure_head = MeasureHead.objects.filter(
            user_defined01__in=all_substation,
            period_rescue=int(year + month),
        ).extra(select_extra).order_by(
            'user_defined01',
            'idclient',
            'idsocket',
            'is_backup',
        ).values()
        measure_head_extra={
            'user_defined01': "SELECT c.user_defined01 from measure_head c where c.id_soc =  "
                             "[measure_detail].[ID_SOC] AND c.is_backup = [measure_detail].[is_backup] "
                             "AND c.period_rescue = %s" % int(year + month),
            'idclient': "SELECT d.idclient from measure_head d where d.id_soc =  "
                              "[measure_detail].[ID_SOC] AND d.is_backup = [measure_detail].[is_backup] "
                              "AND d.period_rescue = %s" % int(year + month),
            'idsocket': "SELECT e.idsocket from measure_head e where e.id_soc =  "
                        "[measure_detail].[ID_SOC] AND e.is_backup = [measure_detail].[is_backup] "
                        "AND e.period_rescue = %s" % int(year + month),

        }
        print("Total de measure_head:" + str(len(measure_head)))
        id_soc_in = [x.get('id_soc') for x in measure_head]


        measure_detail = []
        measure_detail_cn = 0
        if len(id_soc_in) > 0:
            measure_detail_q = MeasureDetail.objects.filter(
                id_soc__in=id_soc_in,
                monthx=month,
                yearx=year
            ).extra(measure_head_extra)
            measure_detail = measure_detail_q.order_by(
                'user_defined01',
                'idclient',
                'idsocket',
                'is_backup',
                'yearx',
                'monthx',
                'dayx',
                'hourx',
                'minute',
                'minute_end'
            ).values()

            measure_detail_cn = measure_detail_q.values('id_soc').annotate(dcount=Count('id_soc')).aggregate(
                Max('dcount')).get('dcount__max')

            len_measure_detail=len(measure_detail)
            print("Total de measure_detail:" + str(len_measure_detail))
            if len_measure_detail >= 0:            # return
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
                print('El filtro seleccionado no tiene datos')
        else:
            print('El filtro seleccionado no tiene datos')

    except Exception as error:
           print("error:" + str(error))

# canales
channels = ChannelConfig.objects.filter(report_field=1, order_field__lte = 4).values().order_by('report_order_field')
channel_quantity = channels.count()

# Lista de subStations
all_substation = Sockets.objects.exclude(user_defined03='').filter(
    Q(user_defined01__startswith='A') | Q(user_defined01__startswith='B') | Q(user_defined01__startswith='C')| Q(user_defined01__startswith='D')
).values_list('user_defined01', flat=True) \
    .distinct().order_by('user_defined01')
letter = ' A-D'
print('------------------------------------------------------------------------------------')
sheet_name = "SUBESTATION" + letter
name_file = sheet_name + "_" + datetime_ce + "." + "xlsx"
substations(all_substation, channels)

# Lista de subStations
all_substation = Sockets.objects.exclude(user_defined03='').filter(
   Q(user_defined01__startswith='E') | Q(user_defined01__startswith='F') | Q(user_defined01__startswith='G')| Q(user_defined01__startswith='H')
  | Q(user_defined01__startswith='I') | Q(user_defined01__startswith='J') | Q(user_defined01__startswith='K')| Q(user_defined01__startswith='L')
  | Q(user_defined01__startswith='M') | Q(user_defined01__startswith='N') | Q(user_defined01__startswith='Ñ') | Q(user_defined01__startswith='O')

).values_list('user_defined01', flat=True) \
    .distinct().order_by('user_defined01')
letter = ' E-O'
print('------------------------------------------------------------------------------------')
sheet_name = "SUBESTATION" + letter
name_file = sheet_name + "_" + datetime_ce + "." + "xlsx"
substations(all_substation, channels)


# Lista de subStations
all_substation = Sockets.objects.exclude(user_defined03='').filter(
   Q(user_defined01__startswith='P') | Q(user_defined01__startswith='Q') | Q(user_defined01__startswith='R')| Q(user_defined01__startswith='S')
  | Q(user_defined01__startswith='T') | Q(user_defined01__startswith='U') | Q(user_defined01__startswith='V')| Q(user_defined01__startswith='W')
  | Q(user_defined01__startswith='X') | Q(user_defined01__startswith='Y') | Q(user_defined01__startswith='Z')
).values_list('user_defined01', flat=True) \
    .distinct().order_by('user_defined01')
letter = ' P-Z'
print('------------------------------------------------------------------------------------')
sheet_name = "SUBESTATION" + letter
name_file = sheet_name + "_" + datetime_ce + "." + "xlsx"
substations(all_substation, channels)
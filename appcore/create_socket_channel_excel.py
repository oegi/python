import os
import sys


import django
import time
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

# los modelo deben ir despues del django.setup()
from appcore.models import SocketChannel
from appcore.helpers.socket import SocketHelper


datetime_ce = time.strftime("%Y%m%d")
datetime_ce1 = time.strftime("%Y%m")
month = time.strftime("%m")#'11'
year = time.strftime("%Y")#'2018'

directory = os.path.join('/SOCKET/', year, month)

print("INICIO DE GENERACION DE ARCHIVO SOCKET_CHANNEL")

if not os.path.exists(directory):
    os.makedirs(directory)
socket_channel = SocketChannel.objects.all().values(
            'id_soc',
            'noins',
            'idsocket',
            'idclient',
            'serialno',
            'user_defined01',
            'user_defined02',
            'user_defined03',
            'user_defined06',
            'user_defined07',
            'user_defined14',
            'user_defined17',
            'user_defined18',
            'min_datetime',
            'max_datetime',
            'user_defined59',
            'num_log',
            'in_energia_act',
            're_energia_act',
            'in_energia_rea',
            're_energia_rea',
            'kwhd',
            'kvarhd',
            'kwhr',
            'kvarhr',
            'vll_ab_mean',
            'vll_bc_mean',
            'vll_ca_mean',
            'ia_mean',
            'ib_mean',
            'ic_mean',
            'vll_avg_mean',
            'iavg_mean',

)
sheet_name = "SOCKET"
name_file = sheet_name + "_" + datetime_ce + "." + "xlsx"

full_path_excel = os.path.join(directory, name_file)

print("full_path_excel:" + str(full_path_excel))
name_file = sheet_name + "_" + datetime_ce + "." + "xlsx"
socket_helper = SocketHelper(
            detail=socket_channel,
        )
socket_helper.save(output=full_path_excel, )

print("*** Generacion SOCKET CHANNEL:" + str(datetime_ce))
print("INICIO DE GENERACION DE ARCHIVO SOCKET_CHANNEL")
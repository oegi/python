from django.shortcuts import render
from django.views.generic import TemplateView

from appcore.models import Questions
from appcore.models import Sockets
from appcore.models import SocketHide


class AdminMedidaView(TemplateView):
    template_name = 'admin_medida.html'

    def get(self, request, *args, **kwargs):
        questions = Questions.objects.filter(category__title='ADMINISTRAR PUNTO DE MEDIDA', is_active=True, )

        clients = Sockets.objects.filter(idclient__isnull=False, description='Real').distinct() \
            .values('idclient').order_by('idclient')

        substations = Sockets.objects.filter(user_defined01__isnull=False, description='Real') \
            .exclude(user_defined01='').distinct().values('user_defined01') \
            .order_by('user_defined01')
        extra_hide = {
            'socket_hide': "SELECT COUNT(1) from socket_hide c where c.idsocket =  "
                              "[sockets].[ID_SOC]"
        }

        sockets = Sockets.objects.filter(idsocket__isnull=False, user_defined01__isnull=False, description='Real') \
            .extra(extra_hide).values('idsocket', 'user_defined01', 'id_soc', 'idclient','socket_hide').order_by('idsocket')

        return render(request, self.template_name, locals())

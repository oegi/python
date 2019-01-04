from django.shortcuts import render
from django.views.generic import TemplateView

from appcore.models import (
    Menu,
    Questions,
    Reason,
    Binnacle,
    SocketHide, Sockets)


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        menus = Menu.objects.filter(is_active=True, ).order_by('order_field')
        questions = Questions.objects.filter(category__title='PREGUNTAS', is_active=True, ).order_by('order_field')
        return render(request, self.template_name, locals())


class BinnacleModifyView(TemplateView):
    template_name = 'modifybinnacle.html'

    def get(self, request, *args, **kwargs):
        datag = request.GET
        menus = Menu.objects.filter(is_active=True, ).order_by('order_field')
        questions = Questions.objects.filter(category__title='BITACORA', is_active=True, ).order_by('-date_created')
        binnacle_id = datag.get('binnacle_id', None)
        binnacle = None
        try:
            binnacle = Binnacle.objects.get(id=binnacle_id)

        except Binnacle.DoesNotExist:
            pass
        reasons = Reason.objects.filter(is_active=True).all()

        return render(request, self.template_name, locals())


class BinnacleGroundsView(TemplateView):
    template_name = 'grounds.html'

    def get(self, request, *args, **kwargs):
        reasons = Reason.objects.filter(is_active=True).order_by('description')
        menus = Menu.objects.filter(is_active=True, ).order_by('order_field')

        questions = Questions.objects.filter(category__title='BITACORA', is_active=True, ).order_by('-date_created')
        return render(request, self.template_name, locals())


class ReportsView(TemplateView):
    template_name = 'reports.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, locals())


class CollectorManualView(TemplateView):
    template_name = 'modules/collector/manual.html'

    def get(self, request, *args, **kwargs):
        socket_hide = SocketHide.objects.values('idsocket')
        clients = Sockets.objects.filter(
            idclient__isnull=False,
            description='Real'
        ).exclude(idsocket__in=[x.get('idsocket') for x in socket_hide]).distinct().values('idclient') \
            .order_by('idclient')

        questions = Questions.objects.filter(
            category__title='RECOLECTOR DE MEDIDAS', is_active=True,
        ).order_by('-date_created')
        return render(request, self.template_name, locals())


class CollectorMeasureView(TemplateView):
    template_name = 'collector.html'

    def get(self, request, *args, **kwargs):
        socket_hide = SocketHide.objects.values('idsocket')
        clients = Sockets.objects.filter(
            idclient__isnull=False,
            description='Real'
        ).exclude(idsocket__in=[x.get('idsocket') for x in socket_hide]).distinct().values('idclient') \
            .order_by('idclient')

        questions = Questions.objects.filter(
            category__title='RECOLECTOR DE MEDIDAS', is_active=True
        ).order_by('-date_created')

        return render(request, self.template_name, locals())

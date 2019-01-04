import json
from datetime import datetime

from django.core.mail import EmailMessage
from django.db import IntegrityError, transaction
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import View

from appcore.helpers import status
from appcore.helpers.exceptions import ErrorException
from appcore.models import Binnacle, Reason, Parameter
from appcore.prime_v10_models import Clients


class InfoView(View):
    http_method_names = ['put', 'post', 'delete', ]

    # save method binnacle
    @method_decorator(ensure_csrf_cookie)
    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        mante_num = data.get('mante_num', None)
        state = data.get('state', None)
        reason_id = None
        try:
            reason = Reason.objects.get(description=data.get('reason', None))
            reason_id = reason.id
        except Reason.DoesNotExist:
            pass

        binnacle = Binnacle.objects.filter(id=data.get('id', None))

        http_response = HttpResponse(json.dumps(
            dict(
                status='error',
                message='Se ha producido un error al actualizar el registro.'
            )
        ), content_type='application/json')
        if reason_id is not None:
            try:
                with transaction.atomic():
                    binnacle.update(
                        comments=data.get('comment', None).strip(),
                        date_update=datetime.now(),
                        reason_id=reason_id,
                        mante_num=mante_num,
                        state=state,
                    )
                http_response = HttpResponse(json.dumps(
                    dict(
                        status='success',
                        message='El registro se actualizado'
                    )
                ), content_type='application/json')
            except IntegrityError:
                pass
        return http_response

    @method_decorator(ensure_csrf_cookie)
    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body)
        id = data.get('id', None)
        Binnacle.objects.filter(id=id).delete()
        return HttpResponse(json.dumps(
            dict(
                status='success',
                message='El registro se actualizado'
            )
        ), content_type='application/json')

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        period_rescue = data.get('period_int', None)
        origin = [data.get('origin', None)]
        state = [data.get('state', None)]

        if '__all__' in period_rescue:
            period_rescue = [x.get('period_rescue') for x in Binnacle.objects.distinct().values('period_rescue')]
        if period_rescue == '':
            period_rescue = [x.get('period_rescue') for x in Binnacle.objects.distinct().values('period_rescue')]

        if '__all__' == data.get('origin', None):
            origin = ['MANUAL', 'PRMTE']

        if [''] == origin:
            origin = ['MANUAL', 'PRMTE']

        if '__all__' == data.get('state', None):
            state = ['PENDIENTE', 'FINALIZADO']

        if state == "PENDIENTE":
            state = ['PENDIENTE']

        select_extra = {
            'drescue': "FORMAT(date_rescue, 'dd-MM-yyyy HH:mm:ss', 'es-CL' )",
            'dstart': "FORMAT(date_start, 'dd-MM-yyyy HH:mm:ss', 'es-CL' )",
            'dend': "FORMAT(date_end, 'dd-MM-yyyy HH:mm:ss', 'es-CL' )",
            'dcreated': "FORMAT(date_created, 'dd-MM-yyyy HH:mm:ss', 'es-CL' )",
            'dupdate': "FORMAT(date_update, 'dd-MM-yyyy HH:mm:ss', 'es-CL' )",
        }

        binnacles = Binnacle.objects.filter(
            period_rescue__in=period_rescue,
            origin__in=origin,
            state__in=state
        ).extra(select=select_extra).values(
            'id',
            'cod_binnacle',
            'period_rescue',
            'noins',
            'origin',
            'user_defined01',
            'user_defined02',
            'user_defined03',
            'idsocket',
            'drescue',
            'dstart',
            'dend',
            'state',
            'dcreated',
            'dupdate'
        )

        return HttpResponse(json.dumps(
            dict(data=list(binnacles))
        ), content_type='application/json')


class ConsultView(View):
    http_method_names = ['post', 'put', ]

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        id = data.get('id', None)
        binnacles = Binnacle.objects.filter(id=id).delete()

        return HttpResponse(json.dumps(
            dict(data=list(binnacles))
        ), content_type='application/json')

    @method_decorator(ensure_csrf_cookie)
    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        mante_num = data.get('mante_num', None)
        state = data.get('state', None)
        reason_id = None
        try:
            reason = Reason.objects.get(description=data.get('reason', None))
            reason_id = reason.id
        except Reason.DoesNotExist:
            pass
        binnacle = Binnacle.objects.filter(id=data.get('id', None))
        http_response = HttpResponse(json.dumps(
            dict(
                status='error',
                message='Se ha producido un error al actualizar el registro.'
            )
        ), content_type='application/json')
        if reason_id is not None:
            try:
                with transaction.atomic():
                    binnacle.update(
                        comments=data.get('comment', None),
                        date_update=datetime.now(),
                        reason_id=reason_id,
                        mante_num=mante_num,
                        state="FINALIZADO",
                    )
                    self.sender_mail(**data)
                http_response = HttpResponse(json.dumps(
                    dict(
                        status='success',
                        message='El registro se actualizado'
                    )
                ), content_type='application/json')
            except IntegrityError:
                pass
        return http_response

    @staticmethod
    def sender_mail(**data):
        date_intervention = data.get('date_intervention')
        date_start = data.get('date_start')
        date_end = data.get('date_end')
        id_binnacle = data.get('id_binnacle')
        id_socket = data.get('id_socket')
        reason = data.get('reason')
        mante_num = data.get('mante_num')
        comment = data.get('comment')

        affair = 'Se ha finalizado la bitacora: {}'.format(id_binnacle)

        sender = 'Cordinador Electrico Nacional <noreply@cordinador.electrico.nacional.cl>'
        status_request = status.HTTP_400_BAD_REQUEST
        mail_to = []

        idclient = data.get('client')
        try:
            parameter = Parameter.objects.get(name='MAIL_TO')
            mail = parameter.value
            if mail is not None:
                mail_to.append(mail)
        except Parameter.DoesNotExist:
            pass

        if idclient is not None:
            try:
                client = Clients.objects.get(idclient=idclient)
                user_defined8 = client.user_defined8
                if user_defined8 is not None:
                    mail_to.append(user_defined8)
                user_defined12 = client.user_defined12
                if user_defined12 is not None:
                    mail_to.append(user_defined12)
            except Clients.DoesNotExist:
                pass

        if len(mail_to) != 0:
            try:
                html = render_to_string('email/binnacle/index.html', {
                    'title': 'Información del Sistema',
                    'id_socket': id_socket,
                    'affair': affair,
                    'date_intervention': date_intervention,
                    'date_start': date_start,
                    'date_end': date_end,
                    'reason': reason,
                    'maintenance_intern': mante_num,
                    'comment': comment,
                    'user': 'Usuario pendiente',
                    'site_url': 'https://medidas.coordinadorelectrico.cl/',
                })
                mail_message = EmailMessage(affair, html, to=mail_to, from_email=sender)
                mail_message.content_subtype = 'html'  # Main content is now text/html
                mail_message.send()
                status_request = status.HTTP_202_ACCEPTED
            except ErrorException:
                pass

        return status_request

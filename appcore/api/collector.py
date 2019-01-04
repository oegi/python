import glob
import json
import os
from datetime import datetime

from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.core.mail import EmailMessage
from django.db import IntegrityError, transaction
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import View

from appcore.helpers import status
from appcore.helpers.exceptions import ErrorException
from appcore.models import Parameter, MtCollectorHistory
from appcore.prime_v10_models import Clients


class CollectorView(View):
    http_method_names = ['post', ]

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):
        files = request.FILES
        data = request.POST
        client = data.get('client')
        measurement = data.get('measurement')
        date_start = data.get('date_start')
        date_end = data.get('date_end')
        email = data.get('email')
        _message = data.get('message')
        attachment = files.get('attachment')
        if date_start is not None and date_start is not '':
            date_start = datetime.strptime(date_start, '%d-%m-%Y %H:%M')
        if date_end is not None and date_end is not '':
            date_end = datetime.strptime(date_end, '%d-%m-%Y %H:%M')
        mt_collector_history = MtCollectorHistory()
        mt_collector_history.date_start = date_start
        mt_collector_history.date_end = date_end
        mt_collector_history.idclient = client
        mt_collector_history.idsocket = measurement
        mt_collector_history.mail = email
        mt_collector_history.message = _message
        observation = 'El archivo {} se ha cargado satisfactoriamente en la siguiente ruta {}'

        observation_html = '<p>El archivo <span style="font-weight: bold;">{}</span> se ha cargado ' \
                           'satisfactoriamente en la siguiente ruta <span style="font-weight: bold;">{}</span>' \
                           '</p>'

        data_response = dict(status=status.HTTP_201_CREATED, content_type='application/json')
        file_name = ''
        path_local = ''

        path_directory = None
        try:
            parameter = Parameter.objects.get(name='DIRECTORY_MEASU_COLLECTOR')
            path_directory = parameter.value
        except Parameter.DoesNotExist:
            observation = 'No se encontró un directorio base, por favor defina un directorio '
            'base para subida de los archivos'
            observation_html = observation
            data_response = dict(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

        if attachment is not '' and attachment is not None and path_directory is not None:
            try:
                file_name = self.upload_file(path_directory=path_directory, file=attachment)
                path_local = os.path.join(path_directory, 'FORMATO_PRMTE')
                mt_collector_history.name_file = file_name
                mt_collector_history.path_file = path_local
            except ErrorException:
                observation = 'No se pudo procesar el archivo, contáctese con el administrador del sitio'
                observation_html = observation
                data_response = dict(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
        if data_response.get('status') == 201:
            observation = observation.format(file_name, path_local)
            observation_html = observation_html.format(file_name, path_local)
        mt_collector_history.observation = observation
        try:
            with transaction.atomic():
                mt_collector_history.save()
        except IntegrityError:
            observation = 'Se ha producido un error al guardar los datos'
            observation_html = observation
            data_response = dict(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

        self.sender_mail(observation_html, _message, **{
            'client': client,
            'measurement': measurement,
            'mail': email,
            'date_start': date_start,
            'date_end': date_end,
            'attachment': os.path.join(path_directory, 'FORMATO_PRMTE', file_name)
        })
        return HttpResponse(json.dumps(dict(message=observation_html)), **data_response)

    @staticmethod
    def upload_file(path_directory: str = '', file: TemporaryUploadedFile = None):
        path_local = os.path.join(path_directory, 'FORMATO_PRMTE')
        name, extension = file.name.split('.')
        file_name = '%s.%s' % (name, extension)
        patch_absolute = os.path.join(path_directory, 'FORMATO_PRMTE', file_name)
        if os.path.isfile(patch_absolute):
            os.chdir(path_local)
            cnt_file = len(glob.glob('{}*'.format(name))) + 1
            file_name = '%s_%s.%s' % (name, cnt_file, extension)
        file_storage = FileSystemStorage(location=path_local)
        file_storage.save(file_name, file)
        return file_name

    @staticmethod
    def sender_mail(observation, _message, **data):
        client = data.get('client')
        attachment = data.get('attachment')
        measurement = data.get('measurement')
        mail = data.get('mail')
        date_start = data.get('date_start')
        date_end = data.get('date_end')
        affair = 'Recolector de Medidas formato PRMTE: {} - Medidor: {}:'.format(client, measurement)
        sender = 'Cordinador Electrico Nacional <noreply@cordinador.electrico.nacional.cl>'

        status_request = status.HTTP_400_BAD_REQUEST

        try:
            html = render_to_string('email/collector/index.html', {
                'title': 'Información del Sistema',
                'client': client,
                'affair': affair,
                'measurement': measurement,
                'date_start': date_start,
                'date_end': date_end,
                'message': _message,
                'observation': observation,
                'user': 'Usuario pendiente',
                'site_url': 'https://medidas.coordinadorelectrico.cl/',
            })
            mail_message = EmailMessage(affair, html, to=mail.split(','), from_email=sender)
            if os.path.isfile(attachment):
                try:
                    mail_message.attach_file(attachment)
                except ErrorException:
                    pass
            mail_message.content_subtype = 'html'  # Main content is now text/html
            mail_message.send()
            status_request = status.HTTP_202_ACCEPTED
        except ErrorException:
            pass
        return status_request


class MailView(View):
    http_method_names = ['post', ]

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):
        data = request.body
        try:
            data = json.loads(data)
        except ErrorException:
            data = None
        mail_to = []
        data_response = dict(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
        if data is not None:
            idclient = data.get('idclient')
            try:
                parameter = Parameter.objects.get(name='MAIL_TO')
                mail = parameter.value
                if mail is not None:
                    mail_to.append(mail)
            except Parameter.DoesNotExist:
                pass
            try:
                client = Clients.objects.get(idclient=idclient)
                user_defined8 = client.user_defined8
                if user_defined8 is not None:
                    mail_to.append(user_defined8)
                user_defined12 = client.user_defined12
                if user_defined12 is not None:
                    mail_to.append(user_defined12)
                mail_to = ', '.join(mail_to)
            except Clients.DoesNotExist:
                pass
            data_response = dict(status=status.HTTP_202_ACCEPTED, content_type='application/json')
        return HttpResponse(json.dumps(dict(data=dict(mail_to=mail_to))), **data_response)

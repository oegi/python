import os
import sys

import django
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

from appcore.models import Binnacle, Parameter

binnacles = Binnacle.objects.filter(state='PENDIENTE').all()
affair = 'Bitácoras Pendientes'
sender = ''

mail_to = ['']

try:
    parameter = Parameter.objects.get(name='MAIL_TO')
    mail = parameter.value
    if mail is not None:
        mail_to.append(mail)
except Parameter.DoesNotExist:
    pass

if len(mail_to) != 0:
    try:
        html = render_to_string('email/binnacle/pending.html', {
            'binnacles': binnacles,
        })
        mail_message = EmailMessage(affair, html, to=mail_to, from_email=sender)
        mail_message.content_subtype = 'html'  # Main content is now text/html
        mail_message.send()
    except Exception as e:
        print(e.args)

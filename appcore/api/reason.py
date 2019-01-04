import json
from datetime import datetime

from django.db import IntegrityError, transaction
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import View

from appcore.models import Reason, Binnacle


class IndexView(View):
    http_method_names = ['put', 'post', 'delete', ]

    @method_decorator(ensure_csrf_cookie)
    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body)
        id = data.get('id', None)
        # reasons = Reason.objects.filter(id=id).delete()
        # Validar que el id no este en alguna binnacle
        exist = Binnacle.objects.filter(reason=id).exists()
        if exist:
            return HttpResponse(json.dumps(
                dict(
                    status='error',
                    message='Error Motivo existe en bitacora.'
                )
            ), content_type='application/json')
        else:
            reasons = Reason.objects.filter(id=id).delete()
            return HttpResponse(json.dumps(
                dict(
                    status='success',
                    message='El registro se elimino'
                )
            ), content_type='application/json')

    @method_decorator(ensure_csrf_cookie)
    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        is_active = data.get('is_active', None)
        description = data.get('description', None)
        reason = Reason.objects.filter(id=data.get('id', None))

        try:
            with transaction.atomic():
                reason.update(
                    is_active=is_active,
                    date_update=datetime.now(),
                    description=description,
                )
        except IntegrityError:
            pass

        return HttpResponse(json.dumps(
            dict(
                status='success',
                message='El registro se actualizado'
            )
        ), content_type='application/json')

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):

        reasons = Reason.objects.filter(is_active=True).values()
        data = list()
        for reason in reasons:
            date_created = reason.get('date_created')
            date_update = reason.get('date_update')
            date_created = (date_created is not None) and date_created.__format__('%d-%m-%Y') or None
            date_update = (date_update is not None) and date_update.__format__('%d-%m-%Y') or None
            data.append({
                'id': reason.get('id'),
                'description': reason.get('description'),
                'is_active': reason.get('is_active'),
                'date_created': date_created,
                'date_update': date_update,
            })
        return HttpResponse(json.dumps(
            dict(
                status='success',
                data=list(data)
            )
        ), content_type='application/json')


class CreateView(View):
    http_method_names = ['post', ]

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):
        #  data = request.POST
        data = json.loads(request.body)
        reason = Reason(
            description=data.get('description')
        )
        try:
            with transaction.atomic():
                reason.save()
        except IntegrityError:
            return HttpResponse(json.dumps(
                dict(
                    status='error',
                    message='Error el registro ya se existe.'
                )
            ), content_type='application/json')

        return HttpResponse(json.dumps(
            dict(
                status='success',
                message='Se ha añadido un nuevo registro satisfactoriamente!',
                data=list(data)
            )
        ), content_type='application/json')

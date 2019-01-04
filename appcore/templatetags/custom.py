from django import template
from django.template.defaultfilters import stringfilter

from appcore.models import Binnacle

register = template.Library()


@register.filter
@stringfilter
def trim(value):
    return value.strip()


@register.simple_tag
def set(data):
    return data


@register.simple_tag
def any_function():
    binnacles = Binnacle.objects.filter(state='PENDIENTE').all()
    return binnacles

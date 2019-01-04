# Note: months may be positive, or negative, but must be an integer.
from datetime import timedelta

_MONTHNAMES = [None, "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
               "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

_DAYNAMES = [None, "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sabádo", "Domingo"]


class DateTimeError(Exception):
    pass


def back_months(date, months):
    target = (date.month - months) + 1

    try:
        date.replace(year=date.year + int(target / 12), month=(target % 12))
    except DateTimeError:
        date.replace(year=date.year + int((target + 1) / 12), month=((target + 1) % 12), day=1)
        date += timedelta(days=-1)

    dictionaries = list()
    while target <= date.month:
        """
          str(calendar.monthrange(date.year, target).__getitem__(1))
        """
        dictionaries.append({
            'key': '{}|{}'.format(target, date.year),
            'value': '{} - {}'.format(_MONTHNAMES[target], date.year),
        })

        target += 1

    return dictionaries


def add_months(date, months):
    target = date.month + months
    try:
        date.replace(year=date.year + int(target / 12), month=(target % 12))
    except DateTimeError:
        date.replace(year=date.year + int((target + 1) / 12), month=((target + 1) % 12), day=1)
        date += timedelta(days=-1)

    return date

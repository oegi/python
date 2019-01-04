"""Microsoft SQL Server database backend for Django."""
from __future__ import absolute_import, unicode_literals

from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.validators import validate_ipv46_address as ip_validator


def make_connection_string(settings):
    db_name = settings['NAME'].strip()
    db_host = settings['HOST'] or '127\x2E0\x2E0\x2E1'
    db_port = settings['PORT']
    db_user = settings['USER']
    db_password = settings['PASSWORD']
    options = settings.get('OPTIONS', {})

    if len(db_name) == 0:
        raise ImproperlyConfigured("You need to specify a DATABASE NAME in your Django settings file.")

    # Connection strings courtesy of:
    # http://www.connectionstrings.com/?carrier=sqlserver

    # If a port is given, force a TCP/IP connection. The host should be an IP address in this case.
    if db_port:
        if not is_ip_address(db_host):
            raise ImproperlyConfigured("When using DATABASE PORT, DATABASE HOST must be an IP address.")
        try:
            db_port = int(db_port)
        except ValueError:
            raise ImproperlyConfigured("DATABASE PORT must be a number.")
        db_host = '{0},{1};Network Library=DBMSSOCN'.format(db_host, db_port)

    # If no user is specified, use integrated security.
    if db_user != '':
        auth_string = 'UID={0};PWD={1}'.format(db_user, db_password)
    else:
        auth_string = 'Integrated Security=SSPI'

    parts = [
        'DATA SOURCE={0};Initial Catalog={1}'.format(db_host, db_name),
        auth_string
    ]

    if not options.get('provider', None):
        options['provider'] = 'sqlncli10'

    parts.append('PROVIDER={0}'.format(options['provider']))

    extra_params = options.get('extra_params', '')

    if 'sqlncli' in options['provider'].lower() and 'datatypecompatibility=' not in extra_params.lower():
        # native client needs a compatibility mode that behaves like OLEDB
        parts.append('DataTypeCompatibility=80')

    if options.get('use_mars', True) and 'mars connection=' not in extra_params.lower():
        parts.append('MARS Connection=True')

    if extra_params:
        parts.append(options['extra_params'])

    return ";".join(parts)


def is_ip_address(value):
    """
    Returns True if value is a valid IP address, otherwise False.
    """
    try:
        ip_validator(value)
    except ValidationError:
        return False
    return True

django-pyodbc-azure
-------------------

    **Features**

    -  Supports Django 2.1
    -  Supports Microsoft SQL Server 2008/2008R2, 2012, 2014, 2016, 2017 and
           Azure SQL Database
    -  Passes most of the tests of the Django test suite
    -  Compatible with
           `Micosoft ODBC Driver for SQL Server <https://docs.microsoft.com/en-us/sql/connect/odbc/microsoft-odbc-driver-for-sql-server>`__,
           `SQL Server Native Client <https://msdn.microsoft.com/en-us/library/ms131321(v=sql.120).aspx>`__,
           and `FreeTDS <http://www.freetds.org/>`__ ODBC drivers

    **Dependencies**

    -  Django 2.1
    -  pyodbc 3.0 or newer

    **Installation**

    1. Install pyodbc and Django

    2. Install django-pyodbc-azure ::

        pip install django-pyodbc-azure

    3. Now you can point the ``ENGINE`` setting in the settings file used by
       your Django application or project to the ``'sql_server.pyodbc'``
       module path ::

        'ENGINE': 'sql_server.pyodbc'

    4. Install the next library in case an exception is generated ::

        'LINUX': 'sudo apt-get install unixodbc unixodbc-dev'

    **Notice**

    This version of *django-pyodbc-azure* only supports Django 2.1.
    If you want to use it on older versions of Django,
    specify an appropriate version number (2.0.x.x for Django 2.0)
    at installation like this: ::

        pip install "django-pyodbc-azure<2.1"


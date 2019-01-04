from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from appcore.helpers.sqlserver import make_connection_string


class ConnectionStringTestCase(TestCase):
    def assertInString(self, conn_string, pattern):
        """
        Asserts that the pattern is found in the string.
        """
        found = conn_string.find(pattern) != -1
        self.assertTrue(found,
                        "pattern \"%s\" was not found in connection string \"%s\"" % (pattern, conn_string))

    def assertNotInString(self, conn_string, pattern):
        """
        Asserts that the pattern is found in the string.
        """
        found = conn_string.find(pattern) != -1
        self.assertFalse(found,
                         "pattern \"%s\" was found in connection string \"%s\"" % (pattern, conn_string))

    @staticmethod
    def get_conn_string(data=None):
        if data is None:
            data = {}

        db_settings = {
            'ENGINE': 'sql_server.pyodbc',
            'NAME': 'db_name',
            'USER': 'user@myserver',
            'PASSWORD': 'password',
            'HOST': 'server.database.windows',
            'PORT': '',
            'OPTIONS': {
                'driver': 'ODBC Driver 17 for SQL Server',
            },
        }

        db_settings.update(data)
        return make_connection_string(db_settings)

    def test_default(self):
        conn_string = self.get_conn_string()
        self.assertInString(conn_string, 'Initial Catalog=db_name')
        self.assertInString(conn_string, '=server.database.windows;')
        self.assertInString(conn_string, 'MARS Connection=True')

    def test_require_database_name(self):
        """Database NAME setting is required"""
        self.assertRaises(ImproperlyConfigured, self.get_conn_string, {'NAME': ''})

    def test_user_pass(self):
        """Validate username and password in connection string"""
        conn_string = self.get_conn_string({'USER': 'akzio', 'PASSWORD': 'cUy53r5R'})
        self.assertInString(conn_string, 'UID=akzio;')
        self.assertInString(conn_string, 'PWD=cUy53r5R;')
        self.assertNotInString(conn_string, 'Integrated Security=SSPI')

    def test_port(self):
        """Test the PORT setting to make sure it properly updates the connection string"""
        self.assertRaises(ImproperlyConfigured, self.get_conn_string, {'HOST': 'myhost', 'PORT': 1433})
        self.assertRaises(ImproperlyConfigured, self.get_conn_string, {'HOST': 'myhost', 'PORT': 'a'})
        conn_string = self.get_conn_string({'HOST': '127\x2E0\x2E0\x2E1', 'PORT': 1433})
        self.assertInString(conn_string, '=127\x2E0\x2E0\x2E1,1433;')

    def test_extra_params(self):
        """Test extra_params OPTIONS"""
        extras = 'ODBC Driver 17 for SQL Server'
        conn_string = self.get_conn_string({'OPTIONS': {'extra_params': extras}})
        self.assertInString(conn_string, extras)


class ConnectionTestCase(TestCase):
    def test_connect_pass(self):
        pass

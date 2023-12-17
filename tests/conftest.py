import pytest
from werkzeug.test import Client
from webkage.application import App
from webkage.http_response import response


app = App()



@pytest.fixture
def client(routes=[], app=app):

    # Tested routes should be a list of tuples containing a path and a view
    # function in each of the tuple
    def _client(routes=[], app=app):
        wsgi = app.wsgi
        wsgi_client = Client(wsgi)
        if routes:
            for route in routes:
                app.add_path(route[0], route[1])
        return wsgi_client
    return _client

  

@pytest.fixture
def static_client(routes=[], app=app):
    def _static_client(app=app, prefix=None, static_dir=None):
        wsgi = app.wsgi
        wsgi_client = Client(wsgi)
        if prefix and static_dir:
            app.set_static(prefix, static_dir)
        return wsgi_client
    return _static_client

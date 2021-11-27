from werkzeug.test import Client
from webkage.application import App
from webkage.http_response import response



app = App()

#Client to stimulate server
def client(routes, app=app):
    #Routes should be a list of tuples containing a path and a view function
    wsgi = app.wsgi
    client_ = Client(wsgi)
    if routes:
        for route in routes:
            app.add_path(route[0], route[1])
    return client_


class BaseView:
    """A class for creating view objects"""

    def __init__(
            self, 
            data = """<html> 
                        </html>
                    """, 
            status_code = "200"
            ):

        self.data = data
        self.status_code = status_code
    

    def common_view(self, ctx):
        data = self.data.encode()
        return response(ctx, self.status_code, data)




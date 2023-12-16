from werkzeug.test import Client
from webkage.http_response import response
from webkage.application import App


app = App()

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

    def set_cookie(self, ctx):
        session = ctx.session["Name"] = "Loki"
        return response(ctx, "200 OK", self.data.encode())



def client(routes=[], app=app):

    #Tested routes should be a list of tuples containing a path and a view function in each of the tuple
    wsgi = app.wsgi
    client_ = Client(wsgi)
    if routes:
        for route in routes:
            app.add_path(route[0], route[1])
    return client_



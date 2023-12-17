from werkzeug.test import Client
from webkage.http_response import response
from webkage.application import App


app = App()

HTML = """<html>
</html>
"""

class BaseView:
    """A class for creating view objects"""

    def __init__(
            self,
            client,
            routes=list(),
            data=HTML,
            status_code="200"
    ):

        self.data = data
        self.status_code = status_code

        #Initialize cookies
        self.client = client([("/", self.set_cookie),] + routes)
        self.client.get("/")

    def common_view(self, ctx):
        data = self.data.encode()
        return response(ctx, self.status_code, data)

    def set_cookie(self, ctx):
        session = ctx.session["Name"] = "Loki"
        return response(ctx, "200 OK", self.data.encode())


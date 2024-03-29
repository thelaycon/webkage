from webkage.http_response import response
from .settings import BaseView


class CookieView(BaseView):
    """ Views to manipulate cookies are implemented here """

    def __init__(self, client):

        super().__init__(client, routes=[("/dashboard", self.flush_cookie), ("/http", self.common_view), ("/nohttp", self.no_httponly), ("/secure", self.secure), ("/nosecure", self.no_secure)])



    def flush_cookie(self, ctx):
        session = ctx.session
        session.flush()
        return response(ctx, "200 OK", self.data.encode())

    def no_httponly(self, ctx):
        session = ctx.session
        session.httponly(False)
        return response(ctx, "200 OK", self.data.encode())

    def secure(self, ctx):
        session = ctx.session
        session.secure(True)
        return response(ctx, "200 OK", self.data.encode())

    def no_secure(self, ctx):
        session = ctx.session
        session.secure(False)
        return response(ctx, "200 OK", self.data.encode())

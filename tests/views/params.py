from webkage.http_response import response
from .settings import BaseView


class ParamView(BaseView):
    """A class for creating view objects"""

    def __init__(self, client):

        super().__init__(client, routes=[("/products/:id", self.params_view), ("/products/", self.queries_view)])


    def params_view(self, ctx):
        param = ctx.params["id"]
        data = """
                    <html>
                        <head></head>
                        <body>{}</body>
                    </html>
                """.format(param)
        return response(ctx, "200", data)

    def queries_view(self, ctx):
        query = ctx.query["name"]
        data = """
                    <html>
                        <head></head>
                        <body>{}</body>
                    </html>
                """.format(query)
        return response(ctx, "200", data)

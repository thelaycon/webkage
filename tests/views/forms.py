from webkage.http_response import response
from .settings import BaseView


class FormView(BaseView):
    """A class for creating view objects"""

    def form_view(self, ctx):
        data = """
                    <html>
                        <head></head>
                        <body>{}</body>
                    </html>
                """
        if ctx.request["method"] == "POST":
            name = ctx.form["name"]
            data = data.format(name)
        return response(ctx, "200", data)



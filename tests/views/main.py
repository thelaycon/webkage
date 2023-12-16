from  webkage.http_response import redirect, json_response
from .settings import BaseView

class MainView(BaseView):
    """A class for creating view objects"""

    def redirect_view(self, ctx):
        return redirect(ctx, "301", "/dashboard")


    def json_view(self, ctx):
        data = {
            "username":"Joe",
            "age":19
            }
        return json_response(ctx, "200", data)




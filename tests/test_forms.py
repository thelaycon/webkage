from  webkage.http_response import response
from test_settings import BaseView, client



class View(BaseView):
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



#All tests should go below
def test_form_view():
    view = View()
    client_ = client([("/products/add", view.form_view),])
    resp = client_.post("/products/add", data={"name":"John Doe"})
    assert resp.status_code == 200
    assert "John Doe" in resp.get_data(as_text=True)

   

from  webkage.http_response import response
from test_settings import BaseView, client



class View(BaseView):
    """A class for creating view objects"""

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




#All tests should go below
def test_params_view():
    view = View()
    client_ = client([("/products/:id", view.params_view),])
    resp = client_.get("/products/1")
    assert resp.status_code == 200
    assert "1" in resp.get_data(as_text=True)

def test_queries_view():
    view = View()
    client_ = client([("/products/", view.queries_view),])
    resp = client_.get("/products/?name=John")
    assert resp.status_code == 200
    assert "John" in resp.get_data(as_text=True)



from  webkage.http_response import response
from views.params import ParamView
from views.settings import client






#All tests should go below
def test_params_view():
    view = ParamView()
    client_ = client([("/products/:id", view.params_view), ("/", view.set_cookie)])
    client_.get("/")
    resp = client_.get("/products/1")
    assert resp.status_code == 200
    assert "1" in resp.get_data(as_text=True)

def test_queries_view():
    view = ParamView()
    client_ = client([("/products/", view.queries_view), ("/", view.set_cookie)]) 
    client_.get("/")
    resp = client_.get("/products/?name=John")
    assert resp.status_code == 200
    assert "John" in resp.get_data(as_text=True)



from webkage.http_response import response
from views.params import ParamView


# All tests should go below
def test_params_view(client):
    view = ParamView(client=client)
    resp = view.client.get("/products/1")
    assert resp.status_code == 200
    assert "1" in resp.get_data(as_text=True)


def test_queries_view(client):
    view = ParamView(client=client)
    resp = view.client.get("/products/?name=John")
    assert resp.status_code == 200
    assert "John" in resp.get_data(as_text=True)

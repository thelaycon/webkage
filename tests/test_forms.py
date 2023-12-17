from webkage.http_response import response
from views.forms import FormView


# All tests should go below
def test_form_view(client):
    view = FormView(client=client)
    resp = view.client.post("/products/add", data={"name": "John Doe"})
    assert resp.status_code == 200
    assert "John Doe" in resp.get_data(as_text=True)

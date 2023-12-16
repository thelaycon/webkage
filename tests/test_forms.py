from  webkage.http_response import response
from views.forms import FormView
from views.settings import client


#All tests should go below
def test_form_view():
    view = FormView()
    client_ = client([("/products/add", view.form_view), ("/", view.set_cookie)])
    client_.get("/")
    resp = client_.post("/products/add", data={"name":"John Doe"})
    assert resp.status_code == 200
    assert "John Doe" in resp.get_data(as_text=True)

   

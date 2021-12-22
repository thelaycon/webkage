import json
import pytest
from  webkage.http_response import redirect, json_response
from webkage.http_response import load
from test_settings import BaseView, client



#Test setup
class View(BaseView):
    """A class for creating view objects"""

    def redirect_view(self, ctx):
        return redirect(ctx, "301", "/dashboard")


    def json_view(self, ctx):
        data = {
            "username":"Joe",
            "age":19
            }
        return json_response(ctx, "200", data)




#All tests should go below
def test_common_view():
    view = View()
    client_ = client([("/", view.common_view),])
    resp = client_.get("/")
    assert resp.status_code == 200


def test_redirect_view():
    view = View()
    client_ = client([("/", view.redirect_view),])
    resp = client_.get("/")
    assert resp.headers["Location"] == "/dashboard"
    assert resp.status_code == 301



def test_status_code_change():
    view = View(status_code="404")
    client_ = client([("/", view.common_view),])
    resp = client_.get("/")
    assert str(resp.status_code) == view.status_code


def test_json_response():
    view = View()
    client_ = client([("/", view.json_view),])
    resp = client_.get("/")
    assert resp.headers["Content-Type"] == "application/json"
    #assert resp.status_code == 200
    assert resp.get_data(as_text=True) == json.dumps(
            {
                "username":"Joe",
                "age":19
                }
            )

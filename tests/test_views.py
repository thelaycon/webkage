import json
from views.main import MainView
from views.settings import client






#All view tests should go below
def test_common_view():
    view = MainView()
    client_ = client([("/", view.common_view),])
    resp = client_.get("/")
    assert resp.status_code == 200


def test_redirect_view():
    view = MainView()
    client_ = client([("/", view.redirect_view),])
    resp = client_.get("/")
    assert resp.headers["Location"] == "/dashboard"
    assert resp.status_code == 301



def test_status_code_change():
    view = MainView(status_code="404")
    client_ = client([("/", view.common_view),])
    resp = client_.get("/")
    assert str(resp.status_code) == view.status_code


def test_json_response():
    view = MainView()
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

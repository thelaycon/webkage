import json
from views.main import MainView


# All view tests should go below
def test_common_view(client):
    view = MainView(client)
    resp = view.client.get("/home")
    assert resp.status_code == 200


def test_redirect_view(client):
    view = MainView(client)
    resp = view.client.get("/page")
    assert resp.headers["Location"] == "/dashboard"
    assert resp.status_code == 301


def test_status_code_change(client):
    view = MainView(client, status_code="404")
    resp = view.client.get("/home")
    assert str(resp.status_code) == view.status_code


def test_json_response(client):
    view = MainView(client)
    resp = view.client.get("/json")
    assert resp.headers["Content-Type"] == "application/json"
    # assert resp.status_code == 200
    assert resp.get_data(as_text=True) == json.dumps(
        {
            "username": "Joe",
            "age": 19
        }
    )

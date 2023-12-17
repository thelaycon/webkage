""" Test for serving static files """


def test_serve_css(static_client):
    client = static_client(prefix="/static/", static_dir="tests/assets")
    resp = client.get("/static/css/style.css")
    assert resp.status_code == 200


def test_serve_image(static_client):
    client = static_client(prefix="/static/", static_dir="tests/assets")
    resp = client.get("/static/images/example.jpg")
    assert resp.status_code == 200


def test_serve_js(static_client):
    client = static_client(prefix="/static/", static_dir="tests/assets")
    resp = client.get("/static/js/example.js")
    assert resp.status_code == 200


def test_serve_favicon(static_client):
    client = static_client(prefix="/static/", static_dir="tests/assets")
    resp = client.get("/static/images/favicon.ico")
    assert resp.status_code == 200

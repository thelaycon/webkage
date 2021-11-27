import pytest
from werkzeug.test import Client
from webkage.application import App


app = App()


def client(app=app, prefix=None, static_dir=None):
    wsgi = app.wsgi
    client_ = Client(wsgi)
    if prefix and static_dir:
        app.set_static(prefix, static_dir)
    return client_



def test_serve_css():
    client_ = client(prefix="/static/", static_dir="assets")
    resp = client_.get("/static/css/style.css")
    assert resp.status_code == 200


def test_serve_image():
    client_ = client(prefix="/static/", static_dir="assets")
    resp = client_.get("/static/images/example.jpg")
    assert resp.status_code == 200


def test_serve_js():
    client_ = client(prefix="/static/", static_dir="assets")
    resp = client_.get("/static/js/example.js")
    assert resp.status_code == 200


def test_serve_favicon():
    client_ = client(prefix="/static/", static_dir="assets")
    resp = client_.get("/static/images/favicon.ico")
    assert resp.status_code == 200



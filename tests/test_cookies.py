from webkage.http_response import response
from webkage.parser import Cookie
from views.cookies import CookieView


def test_set_cookie(client):
    view = CookieView(client)
    cookie = Cookie()
    resp = view.client.get("/")
    cookie.load(resp.headers["Set-Cookie"])
    assert cookie["Name"].value == "Loki"


def test_flush_cookie(client):
    view = CookieView(client)
    cookie = Cookie()
    resp = view.client.get("/")
    cookie.load(resp.headers["Set-Cookie"])
    assert cookie["Name"].value == "Loki"

    resp = view.client.get("/dashboard")
    cookie = Cookie()
    cookie.load(resp.headers["Set-Cookie"])
    assert "Loki" not in cookie.keys()


def test_httponly(client):
    view = CookieView(client)
    resp = view.client.get("/http")
    assert "HttpOnly" in resp.headers["Set-Cookie"]


def test_no_httponly(client):
    view = CookieView(client)
    resp = view.client.get("/nohttp")
    assert "HttpOnly" not in resp.headers["Set-Cookie"]


def test_secure(client):
    view = CookieView(client)
    
    resp = view.client.get("/secure")
    assert "Secure" in resp.headers["Set-Cookie"]

    resp = view.client.get("/nosecure")
    assert "Secure" not in resp.headers["Set-Cookie"]

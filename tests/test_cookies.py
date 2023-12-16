from webkage.http_response import response
from webkage.parser import Cookie
from views.settings import client
from views.cookies import CookieView





def test_set_cookie():
    view = CookieView()
    client_ = client([("/", view.set_cookie),])
    resp = client_.get("/")
    cookie = Cookie()
    cookie.load(resp.headers["Set-Cookie"])
    assert cookie["Name"].value == "Loki"


def test_flush_cookie():
    view = CookieView()
    client_ = client([("/", view.set_cookie), ("/dashboard", view.flush_cookie), ("/home", view.common_view),])
    resp = client_.get("/")
    cookie = Cookie()
    cookie.load(resp.headers["Set-Cookie"])
    assert cookie["Name"].value == "Loki"

    resp = client_.get()
    cookie = Cookie()
    cookie.load(resp.headers["Set-Cookie"])
    assert cookie["Name"].value == "Loki"

    resp = client_.get("/dashboard")
    cookie = Cookie()
    cookie.load(resp.headers["Set-Cookie"])
    assert "Loki" not in cookie.keys()


def test_httponly():
    view = CookieView()
    client_ = client([("/", view.common_view),])
    resp = client_.get("/")
    cookie = Cookie()
    assert "HttpOnly" in resp.headers["Set-Cookie"]


def test_no_httponly():
    view = CookieView()
    client_ = client([("/", view.no_httponly),])
    resp = client_.get("/")
    cookie = Cookie()
    assert "HttpOnly" not in resp.headers["Set-Cookie"]


def test_secure():
    view = CookieView()
    client_ = client([("/", view.secure), ("/home", view.no_secure),])
    resp = client_.get("/")
    cookie = Cookie()
    assert "Secure" in resp.headers["Set-Cookie"]

    resp = client_.get("/home")
    cookie = Cookie()
    assert "Secure" not in resp.headers["Set-Cookie"]



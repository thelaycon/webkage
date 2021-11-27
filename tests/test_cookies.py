from webkage.application import App
from webkage.http_response import response
from webkage.parser import Cookie
from test_settings import BaseView, client


app = App()


class View(BaseView):
    """ Views to manipulate cookies are implemented here """
    
    def set_cookie(self, ctx):
        session = ctx.session["Name"] = "Ay"
        return response(ctx, "200 OK", self.data.encode())

    def flush_cookie(self, ctx):
        session = ctx.session
        session.flush()
        return response(ctx, "200 OK", self.data.encode())

    def no_httponly(self, ctx):
        session = ctx.session
        session.httponly(False)
        return response(ctx, "200 OK", self.data.encode())

    def secure(self, ctx):
        session = ctx.session
        session.secure(True)
        return response(ctx, "200 OK", self.data.encode())

    def no_secure(self, ctx):
        session = ctx.session
        session.secure(False)
        return response(ctx, "200 OK", self.data.encode())





def test_set_cookie():
    view = View()
    client_ = client([("/", view.set_cookie),])
    resp = client_.get("/")
    cookie = Cookie()
    cookie.load(resp.headers["Set-Cookie"])
    assert cookie["Name"].value == "Ay"


def test_flush_cookie():
    view = View()
    client_ = client([("/", view.set_cookie), ("/dashboard", view.flush_cookie), ("/home", view.common_view),])
    resp = client_.get("/")
    cookie = Cookie()
    cookie.load(resp.headers["Set-Cookie"])
    assert cookie["Name"].value == "Ay"

    resp = client_.get("/home")
    cookie = Cookie()
    cookie.load(resp.headers["Set-Cookie"])
    assert cookie["Name"].value == "Ay"

    resp = client_.get("/dashboard")
    cookie = Cookie()
    cookie.load(resp.headers["Set-Cookie"])
    assert "Ay" not in cookie.keys()


def test_httponly():
    view = View()
    client_ = client([("/", view.common_view),])
    resp = client_.get("/")
    cookie = Cookie()
    assert "HttpOnly" in resp.headers["Set-Cookie"]


def test_no_httponly():
    view = View()
    client_ = client([("/", view.no_httponly),])
    resp = client_.get("/")
    cookie = Cookie()
    assert "HttpOnly" not in resp.headers["Set-Cookie"]


def test_secure():
    view = View()
    client_ = client([("/", view.secure), ("/home", view.no_secure),])
    resp = client_.get("/")
    cookie = Cookie()
    assert "Secure" in resp.headers["Set-Cookie"]

    resp = client_.get("/home")
    cookie = Cookie()
    assert "Secure" not in resp.headers["Set-Cookie"]



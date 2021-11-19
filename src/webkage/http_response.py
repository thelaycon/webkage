"""This module handles and parses http responses. """

from .parser import set_cookie_header
import json
import jinja2



def response(context, status, data):
    """This method should be returned at the end of your views. All three arguments are compulsory and must be specified.


    #main.py
    ...

    def home(ctx):
        ...
        return response(ctx, ""200 OK", myData)

    ...

    """
    content_type = "text/html"
    set_cookie = set_cookie_header(context.session)
    header = [("Content-Type", content_type),] + set_cookie
    start_response = context.response["start_response"]
    start_response(status+" ", header)
    return data


def json_response(context, status, data):
    """Pure JSON objects can be returned as a response by invoking this method. The second argument should be a Pythonic object that can be converted to JSON by the json library."""
    content_type = "application/json"
    set_cookie = set_cookie_header(context.session)
    header = [("Content-Type", content_type),] + set_cookie
    start_response = context.response["start_response"]
    start_response(status+" ", header)
    return jsonify(data)


def static_response(context, status, data):
    """A dummy method that serves static files to the client. This function is invoked by the App module to serve static files."""
    content_type = context.request["content-type"]
    header = [("Content-Type", content_type),]
    start_response = context.response["start_response"]
    start_response(status, header)
    return data


def load(path, data=""):
    """"This method searches for template(HTML) files under ./templates directory relative to where the python file that contains the WSGI entry point lies. Data are enconded and rendered by Jinja2."""
    loader = jinja2.FileSystemLoader(searchpath="./templates")
    env = jinja2.Environment(loader=loader)
    template = env.get_template(path)
    data_ = template.render(data).encode("utf-8")
    return data_


def jsonify(obj):
    """Return Python objects as JSON (in bytes)."""
    jsonified = "{}".format(json.dumps(obj)).encode()
    return jsonified


def redirect(context, status, uri):
    """A HTTP redirect can be invoked by calling this method.


    #main.py
    ...

    def home(ctx):
        ...
        return redirect(ctx, "301 Redirect", "/dashboard")
    """
    header = [("Location", uri)]
    start_response = context.response["start_response"]
    start_response(status+" ", header)
    return b""



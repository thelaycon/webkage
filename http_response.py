# Response module
from .parser import set_cookie_header
import json
import jinja2



def response(context, status, data):
    """ Set Header and start response """
    content_type = context.response["content-type"]
    set_cookie = set_cookie_header(context.session)
    header = [("Content-Type", content_type),] + set_cookie
    start_response = context.response["start_response"]
    start_response(status, header)
    return data


def json_response(context, status, data):
    """ Set Header and start response """
    content_type = "application/json"
    set_cookie = set_cookie_header(context.session)
    header = [("Content-Type", content_type),] + set_cookie
    start_response = context.response["start_response"]
    start_response(status, header)
    return jsonify(data)


def static_response(context, status, data):
    """ Set Header and start static response """
    content_type = context.request["content-type"]
    header = [("Content-Type", content_type),]
    start_response = context.response["start_response"]
    start_response(status, header)
    return data


def load(path, data=""):
    loader = jinja2.FileSystemLoader(searchpath="./templates")
    env = jinja2.Environment(loader=loader)
    template = env.get_template(path)
    data_ = template.render(data).encode("utf-8")
    return data_


def jsonify(obj):
    """ Return Python obj as Json bytes """
    jsonified = "{}".format(json.dumps(obj)).encode()
    return jsonified


def redirect(context, status, uri):
    """ Function to redirect users to new location """
    header = [("Location", uri)]
    start_response = context.response["start_response"]
    start_response(status, header)
    return b""



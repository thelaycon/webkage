# Response module
from config import template_dir
from parser import set_cookie_header



def response(context, status, data):
    """ Set Header and start response """
    content_type = context.request["content-type"]
    set_cookie = set_cookie_header(context.session)
    header = [("Content-Type", content_type),] + set_cookie
    start_response = context.response["start_response"]
    start_response(status, header)
    return data


def static_response(context, status, data):
    """ Set Header and start static response """
    content_type = context.request["content-type"]
    header = [("Content-Type", content_type),]
    start_response = context.response["start_response"]
    start_response(status, header)
    return data


def encode_html(path):
    path = template_dir + "/" + path
    try:
        with open(path, "rb") as f:
            data = f.read()
    except FileNotFoundError:
        raise Exception("Template cannot be found")
    return data


def redirect(context, status, uri):
    header = context.response["header"]
    header["Location"] = uri
    start_response = context.response["start_response"]
    start_response(status, list(header.items()))
    return b""



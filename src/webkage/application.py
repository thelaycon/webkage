""" The application module provides an interface for WSGI servers and other important functions specified in the App class."""


from wsgiref.simple_server import make_server
from .parser import  Context
from . import router
from .http_response import response, static_response, load



class App(object):
    """The App class encapsulates the neccessary functions needed to make the framework compatible with WSGI servers. This is basically the backbone of Webkage.
    The self.wsgi is the interface by which a Webkage app can be served by WSGI compatible servers. In development, the self.serve function can be used in place of a standard WSGI server."""
    def __init__(self):
        self.routes_func = []
        self.routes_no_func = []
        self.static_path_prefix = '--'
        self.static_dir = ''


    def match_route(self, context):
        """This method aims to differentiate between requests for static files vs others. You won't and shouldn't invoke this method."""

        global resp


        path = context.request["path"]
        #Check if static
        if path.startswith(self.static_path_prefix):
            resp = self.serve_static(context, path)
        else:
            if path[-1] != "/":
                path += "/"
            resp = self.serve_response(context, path)

        return resp
       


    def serve_response(self, context, path):
        """This method return a HTTP response back to the client.
        It checks if the requested path matches with any path registered using self.add_path. If none, a 404 page is served using self.not_found. """
        global response_

        matched_route = router.match_route(self.routes_no_func, path)
        if matched_route == None:
            response_ = not_found(context)
        else:
            id_, slug = router.get_params(matched_route, path)
            context.params["slug"] = slug
            context.params["id"] = id_
            for route in self.routes_func:
                if route[0] == matched_route:
                    response_ = route[1](context) #Execute view function
        return response_ 




    def wsgi(self, environ, start_response):
        """This is the WSGI main entry point. All WSGI servers should reference this point.

        Here's an example with Gunicorn:

        #main.py

        from webkage.application import App
        from webkage.http_response import response

        ...

        app = App
        wsgi = app.wsgi

        $gunicorn main:app.wsgi
        """

        context_ = Context(environ)
        context_.response["start_response"] = start_response
        response = self.match_route(context_)
        yield response


    def set_static(self, static_path_prefix, static_dir):
        """The first argument specifies the prefix of all static files while the second argument specifies which directory to serve them from."""
        self.static_path_prefix = static_path_prefix
        if static_dir[-1] != '/':
            self.static_dir = static_dir + '/'


    def serve_static(self, context, path):
        """Unlike self.serve_response, this method serves only static files to the client."""
        file_path = self.static_dir + path.replace(self.static_path_prefix, '').rstrip("/")
        status = "200 OK"
        try:
            with open(file_path, "rb") as file_:
                static_file = file_.read()
            if file_path.endswith(".css"):
                context.request["content-type"] = "text/css"
        except Exception as e:
            static_file = b''
            status = "404 NOT FOUND"
        return static_response(context, status, static_file)


    def add_path(self, uri, method):
        """Use this method to register all paths that should be discoverable by Webkage. Simple paths or complicated ones with parameters can be specified.

        #main.py

        ...

        app = App


        def home(ctx):
            ...

        app.add_path("/home", home)

        ...

        """

        if uri[-1] != "/":
            uri += "/"
        uri = router.path_to_regex(uri)
        path = (uri, method)
        self.routes_func.append(path)
        self.routes_no_func.append(uri)


    def serve(self, host="127.0.0.1", port=8000):
        """Serve App locally. Avoid using it in production, should be disabled before deployment."""

        httpd = make_server(host, port, self.wsgi)
        print("Listening on %s:%d" %(host, port))
        httpd.serve_forever()




def not_found(context):
    """ 404 response view """
    try:
        data = load("404.html")
    except:
        data = b"""
        <html>
            <head>
                    <title>404 Not Found</title>
            </head>
            <body>
            <h2>404 Not Found</h2>
            </body>
        </html>
        """
    return response(context, "404 NOT FOUND", data)



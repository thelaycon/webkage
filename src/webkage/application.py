""" The Application module provides an interface for WSGI """


from wsgiref.simple_server import make_server
from .parser import  Context
from . import router
from .http_response import response, static_response, load



class App(object):
    def __init__(self):
        self.routes_func = []
        self.routes_no_func = []
        self.static_path_prefix = '--'
        self.static_dir = ''


    def match_route(self, context):
        """Function to match response function for a given request"""

        global resp

        path = context.request["path"]
        if path[-1] != "/":
            path += "/"

        #Check if static
        if path.startswith(self.static_path_prefix):
            resp = self.serve_static(context, path)
        else:
            resp = self.serve_response(context, path)
        return resp
       


    def serve_response(self, context, path):
        """Method to serve HTTP response"""
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
                    response_ = route[1](context)
        return response_ 




    def wsgi(self, environ, start_response):
        """ WSGI entry point"""

        context_ = Context(environ)
        context_.response["start_response"] = start_response
        response = self.match_route(context_)
        yield response


    def set_static(self, static_path_prefix, static_dir):
        """Set static directory to serve from and path prefix"""
        self.static_path_prefix = static_path_prefix
        if static_dir[-1] != '/':
            self.static_dir = static_dir + '/'


    def serve_static(self, context, path):
        """ Method to serve static files """
        file_path = self.static_dir + path.replace(self.static_path_prefix, '').rstrip("/")
        status = "200 OK"
        try:
            with open(file_path, "rb") as file_:
                static_file = file_.read()
                if file_path.endswith(".css"):
                    context["content-type"] = "text/css"
        except Exception as e:
            static_file = b''
            status = "404"
        return static_response(context, status, static_file)


    def add_path(self, uri, method):
        """ Adds and register routes """

        if uri[-1] != "/":
            uri += "/"
        uri = router.path_to_regex(uri)
        path = (uri, method)
        self.routes_func.append(path)
        self.routes_no_func.append(uri)


    def serve(self, host="127.0.0.1", port=8000):
        """ Serve App locally. Not suitable for production """

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


# App class instantiation
App = App()

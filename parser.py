# Parser module to parse environ variables
from http.cookies import SimpleCookie
import io
import cgi
import re
import json


def clean(item):
    if item != "":
        return True

def set_cookie_header(cookie):
    """Parse cookie object to HTTP Set-Cookie header"""

    header = list()
    cookie_options = cookie.output().split("Set-Cookie:")
    cookie_options = list(filter(clean, cookie_options))
    for index, option in enumerate(cookie_options):
        cookie_options[index] = option.strip("\r\n")
    cookie_options = ",".join(cookie_options) + '; ' + ';'.join(cookie.options)
    

    header = [("Set-Cookie", cookie_options),]
    return header




class Cookie(SimpleCookie):
    """Cookie class inheriting http.SimpleCookie class"""

    def __init__(self):
        super().__init__()
        self.options = ["HttpOnly",]

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        item = self.__getitem__(key)

    def httponly(self, choice):
        """Set httponly option in Set-Cookie"""
        if choice == True:
            if not "HttpOnly" in self.options:
                self.options.append("HttpOnly")
        elif choice == False:
            if "HttpOnly" in self.options:
                self.options.remove("HttpOnly")


    def secure(self, choice):
        if choice == True:
            if not "Secure" in self.options:
                self.options.append("Secure")
        elif choice == False:
            if "Secure" in self.options:
                self.options.remove("Secure")
    


    
    def flush(self):
        """Expires a given cookie value"""

        self.options.append("expires=Mon 23 Jun 1967 04:34:23 GMT")

    def will_expire(self, date):
        """Sets future expiry date for cookie value"""

        self.options.append("expires={}".format(date))







class Context():
    """Make needed environ variables accessible in a single class"""

    def __init__(self, environ):

        #Get incoming cookies
        cookie = environ.get("HTTP_COOKIE", "")
        self.session = Cookie()
        self.session.load(cookie)

        #HTTP Request
        self.request = dict()
        self.request["content-length"] = environ.get("CONTENT_LENGTH", 0)
        self.request["content-type"] = environ.get("CONTENT_TYPE", "text/html")
        self.request["user-agent"] = environ.get("HTTP_USER-AGENT", "")
        self.request["ip-address"] = environ.get("REMOTE_ADDR", "")
        self.request["path"] = environ.get("PATH_INFO", "/")
        self.query_str = environ.get("QUERY_STRING")
        self.request["method"] = environ.get("REQUEST_METHOD")
        self.request["protocol"] = environ.get("SERVER_PROTOCOL", "")
        self.request["scheme"] = environ.get("wsgi.url_scheme", "http")
        self.request["data"] = environ.get("wsgi.input", "")


        #HTTP Response dict
        self.response = dict()
        self.response["content-type"] = self.request["content-type"]

        #HTTP Parameters dict()
        self.params = dict()

        if self.request["content-length"] == '':
            self.request["content-length"]=0

        #HTTP Form
        #Parse form content
        self.form = dict()
        self.formFile = dict()
        self.json = ''
        fp = self.request["data"].read(int(self.request["content-length"]))
        if self.request["content-type"] == "application/x-www-form-urlencoded":
            formValues = cgi.FieldStorage(fp=io.BytesIO(fp), environ=environ, keep_blank_values=True)
            keys = formValues.keys()
            for key in keys:
                value = formValues[key]
                if value.filename:
                    self.formFile[key] = value
                else:
                    self.form[key] = formValues.getvalue(key)
        elif self.request["content-type"] == "application/json":
            #Process Json request
            self.json = json.loads(fp.decode())


        
        
        #Query matching and parsing
        self.query = dict()

        query_regex = "[a-zA-Z0-9%+]+=[a-zA-Z0-9%+]+"
        queries = re.findall(query_regex, self.query_str)
        for index, query in enumerate(queries):
            queries[index] = query.replace("%20", " ").replace("+", " ")
        
        #Populate Query dict
        for query in queries:
            q = query.split("=")
            self.query[q[0]] = q[1]




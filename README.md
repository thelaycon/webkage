![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg) ![tests](badges/tests.svg) ![coverage](badges/coverage.svg) 


Webkage is a fast and lightweight Python webframework.

It was created with the Python standard library and no external dependencies (except Jinja2).

Webkage's philosophy is simlilar to that of Golang's http library. It emphasizes flexibility and full control.

# Tests

Relies on Pytest and Werkzeug testing client for Unit testing.

```
$ pip install werkzeug pytest
$ cd tests
$ pytest .

```


# Table Of Contents

=====================


* [Introduction](#introduction)
* [Routing](#routing)
* [Static Files](#static-files)
* [Views](#views)
* [Middlewares](#middlewares)
* [Url Parameters](#url-parameters)
* [Url Query](#url-query)
* [Form](#form)
* [Form Files](#form-files)
* [Json Request & Response](#json-request--response)
* [Session and Cookies](#sion-and-cookies)
* [Redirects](#redirects)
* [Templates](#templates)
* [HTTP Request header](#http-request-header)
* [CSRF Tokens](#csrf-tokens)



## Introduction

Creating a web application is simple. The developer first import an instance of the WSGI application and registers a route.


```
app.py


from webkage.application import App
from http_response import load, response

App = App()

def home(ctx):
    resp = load("home.html")
    return response(ctx, "200 OK", resp)


App.add_path("/", home)

#Run server
App.serve()

```

**Always start the route pattern with "/"**

This would spin up a development WSGI server that listens on **127.0.0.1:8000**

This is a development server and it's not suitable for production. For a production based WSGI web server, the entry point for the WSGI App can be accessed via the `wsgi` attribute.

Example using gunicorn.

```
app.py


from webkage.application import App
from http_response import load, response

App = App()

def home(ctx):
    resp = load("home.html")
    return response(ctx, "200 OK", resp)


App.add_path("/", home)

wsgi = App.wsgi

```

Serving the App through gunicorn:

```
$ gunicorn app:wsgi

```


## Routing

In Webkage, routes must be registered using the ```add_path``` method of the application instance. It accepts two compulsory arguments; the path and view function.


```
app.py

...

def home(ctx):
   ...

def login(ctx):
   ...

## Register routes
App.add_path("/", home)
App.add_path("login/", login)


...

```

Url parameters like id and slug can also be used in routes.


```
app.py

...

App.add_path("product/:id/", productIdDetail)
App.add_path("product/:slug/", productSlugDetail)

...

```

The values of these parameters can be accessed in the view function.


## Static Files

In Webkage, static files are served by first registering the directory from which the files will be served from. The `set_static` method is responsible for this.

```
app.py

from webkage.application import App


...

# Serve static
App.set_static("/static/", "static")

...

```

The first argument is the prefix of all static files to be served. The last argument is the directory from which the static files reside.


## Views

While registering routes, views must be assigned to the routes.

A view function is a simple function with just one parameter and returns an http response using either **webkage.http_response.response** or **webkage.http_response.json_response**.

Both of these functions accept three compulsory arguments.

```
app.py

from webkage.http_response import json_response, response, load

...


def home(ctx):
    resp = load("home.html")
    return response(ctx, "200 OK", resp)


def json_home(ctx):
   resp = {"Name":"Uzumaki", "Title":"Hokage"}
   return json_response(ctx, "200 OK", resp)

...

```

The three arguments of both response functions are context object, status code and http reponse object.

List of http response codes can be accessed via http.HTTPStatus module.

**response** function returns a `text/html` response while **json_response** returns a ``application/json` response to the client.



## MiddleWares

Middlewares can be achieved through decorators or high level functions.

```
app.py

...

def auth_middleware(func):
   def new_view(ctx):
      #perform actions here
      return func(ctx)
   return new_view


@auth_middleware
def dashboard(ctx):
   ...


App.add_path("dashboard/", dashboard)

...

```

Or

```
app.py

...

def auth_middleware(func):
   def new_view(ctx):
      #perform actions here
      return func(ctx)
   return new_view



def dashboard(ctx):
   ...


App.add_path("dashboard/", auth_middleware(dashboard))

...

```


## Url Parameters

Url parameters can be accessed via the Context object's `params` attribute.


```
app.py

...


def product(ctx):
   product_id = ctx.params["id"]
   ...

App.add_path("product/:id", product)

...

```


## Url Query 

Url queries can be accessed via the Context object's `query` attribute.

Same process used in accessing Url parameters.


```
app.py

...


def product(ctx):
   product_id = ctx.query["id"]
   ...

App.add_path("product/", product)

...

```


## Form 

Form values can be accessed via the context object's `form` attribute.


```
app.py

...


def add_product(ctx):
   if ctx.request["method"] == "POST":
      product_name = ctx.form["name"]
   ...

App.add_path("product/add", add_product)

...

```


Files uploaded cannot be accessed via the `form` attribute.


## Form Files

Files uploaded via HTTP forms can be accessed the Context object's `formFile` attribute.


```
app.py

...


def new_ca(ctx):
   csv_file = ctx.formFile["csv_file"]
   
   #Access file's name via the filename attribute
   with open(csv_file.filename, "wb") as f:
       f.write(f.read())
   ...

App.add_path("ca/add", new_cases)

...

```


## Json Request & Response

Json objects can be accessed the Context object's `json` attribute; the value is a valid Python dictionary object.

Json response should be done with **webkage.http_response.json_response**, else the returned response will be in "text/html".



## Session and Cookies

Webkage has no provision for File or Database based sions. It's solely a client-based one. All Cookies are HttpOnly by default.


**Setting Cookies' value**


```
app.py

...

def login(ctx):
   ctx.session["name"] = "Rock Lee"
   ...


```

**Setting Cookies to secured only**

```
app.py

...

def login(ctx):
    ctx.session["name"] = "Sakura"
    ctx.secure(True)
    ...

...

```

**Setting Cookies To HttpOnly or not**

```
app.py

...

def login(ctx):
    ctx.session["user"] = 45
    ctx.httponly(False)
    ...

...

```

**Setting Cookies' expiry**

```
app.py

...

def login(ctx):
   ctx.session["user"] = 56
   ctx.will_expire("21 Oct 2015 07:28:00 GMT")
   ...

...

```

**Flushing/Deleting Cookies' session**

```
app.py

...

def logout(ctx):
    ctx.flush()
    ...

...

```

## Redirects

Both Permanent and Temporary redirects can be acheived by specifying the right status code. Redirect can be acheived via **wekage.http_response.redirect**

```
app.py

from webkage.http_response import redirect
...

def secret(ctx):
    return redirect(ctx, "301", "/home")
    ...

...

```


## Templates

Webkage's Templates are powered by Jinja2's templating engine. Templates are expected to reside in `./templates` directory relatively to the module or file in which the views reside.

An example directory will look like:

```
program/
    app.py
    templates/
        home.html

```

In `home.html`, we might have:

```
home.html

<html>
   <head>
       <title>Home</title>
   </head>
   <body>
       <ul>
           {% for item in items %}
           <li>{{ item }}</li>
           {% endfor %}
       </ul>
   </body>
</html>

```

In `app.py`, we might have:

```
app.py

from webkage.http_response, import load, response

...

def items_list(ctx):
    data = {"items":["Shuriken", "Wood", "Boot", "Scroll"]}
    resp = load("home.html", data)
    return response(ctx, "200", resp)

...

```


## HTTP Request Header

The Context object's `request` objects contain the following keys:


```
ctx.request[key]

``` 

**content-length** Length of HTTP request's body.

**content-type** HTTP requests' content type.

**ip-address** Client's IP address.

**user-agent** Client's user agent.

**method** Request method. Either of POST, GET, PUT, or DELETE.

**protocol** Mostly HTTP.

**scheme** Http, Https, etc.


## CSRF Tokens

Webkage does not implement CSRF tokens by default, users who are not building microservices can implement a Middleware to handle this.

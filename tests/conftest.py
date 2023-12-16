import pytest
from werkzeug.test import Client
from webkage.application import App
from webkage.http_response import response



app = App()


class BaseView:
    """A class for creating view objects"""

    def __init__(
            self, 
            data = """<html> 
                        </html>
                    """, 
            status_code = "200"
            ):

        self.data = data
        self.status_code = status_code
    

    def common_view(self, ctx):
        data = self.data.encode()
        return response(ctx, self.status_code, data)




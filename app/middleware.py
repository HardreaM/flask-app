from werkzeug.wrappers import Request
from werkzeug.wrappers import Response
from werkzeug.wrappers import ResponseStream

class Middleware():

    def __call__(self, environ, start_response):

        pass
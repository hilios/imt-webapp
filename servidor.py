import webapp2

from api import DevicesHandler, DeviceMedidasHandler
from static import StaticHandler


class HelloWorld(webapp2.RequestHandler):
    def get(self):
        self.response.write('Ola mundo!')


ROUTES = [
    ('/', HelloWorld),
    ('/static/(.+)', StaticHandler),
    ('/api/devices', DevicesHandler),
    ('/api/devices/(.+)', DeviceMedidasHandler),
]


app = webapp2.WSGIApplication(ROUTES, debug=True)


if __name__ == '__main__':
    from paste import httpserver
    httpserver.serve(app)

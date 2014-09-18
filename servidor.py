import webapp2

from api import DevicesHandler, MedidasDeviceHandler
from static import StaticHandler
from webapp2_extras import jinja2


class HelloWorld(webapp2.RequestHandler):
    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def get(self):
        tmpl = self.jinja2.render_template('index.html')
        self.response.write(tmpl)


ROUTES = [
    ('/', HelloWorld),
    ('/static/(.+)', StaticHandler),
    ('/api/devices', DevicesHandler),
    ('/api/devices/(.+)', MedidasDeviceHandler),
]


app = webapp2.WSGIApplication(ROUTES, debug=True)


if __name__ == '__main__':
    from paste import httpserver
    httpserver.serve(app)

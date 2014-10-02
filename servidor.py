import webapp2
import models

from api import DevicesHandler, MedidasDeviceHandler
from static import StaticHandler
from webapp2_extras import jinja2


class HelloWorld(webapp2.RequestHandler):
    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def get(self, device_id=None):
        tmpl = self.jinja2.render_template('index.html',
            devices=models.Devices.get_all(),
            current_device=models.Devices.get_by_id(device_id)
        )
        self.response.write(tmpl)


ROUTES = [
    ('/(\d+)?', HelloWorld),
    ('/static/(.+)', StaticHandler),
    ('/api/devices', DevicesHandler),
    ('/api/devices/(.+)', MedidasDeviceHandler),
]


app = webapp2.WSGIApplication(ROUTES, debug=True)


if __name__ == '__main__':
    from paste import httpserver
    httpserver.serve(app)

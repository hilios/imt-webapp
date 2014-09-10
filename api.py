import json
import webapp2
import sqlite3
import models

# from datetime import datetime

class DevicesHandler(webapp2.RequestHandler):

    def get(self):
        'Retorna todos os devices registrados'
        devices = models.Devices.get_all()

        self.response.content_type = 'application/json'
        self.response.write(json.dumps(devices))

    def post(self):
        'Cria um novo device'
        device = models.Devices(nome=self.request.params.get('nome'))
        device.save()

        self.response.status = 201

    def put(self):
        id = self.request.params.get('id')
        device = models.Devices.get_by_id(id)

        if not device:
            self.abort(404)

        device['nome'] = self.request.params.get('nome')
        device.save()

        self.response.status = 204

    def delete(self):
        id = self.request.params.get('id')
        device = models.Devices.get_by_id(id)

        if not device:
            self.abort(404)

        device.delete()

        self.response.status = 204


class DeviceMeasuresHandler(webapp2.RequestHandler):
    def get(self, device_id):
        device = models.Devices.get_by_id(device_id)

        if not device:
            self.abort(404)

        measures = device.measures()

        self.response.content_type = 'application/json'
        self.response.write(json.dumps(measures))


    def post(self, device_id):
        device = models.Devices.get_by_id(device_id)

        if not device:
            self.abort(404)

        measure = models.Measures(
            device_id=device_id,
            temperatura=self.request.params.get('temperatura'),
            humidade=self.request.params.get('humidade'),
            lat=self.request.params.get('lat'),
            lng=self.request.params.get('lng')
        )

        measure.save()

        self.response.status = 204

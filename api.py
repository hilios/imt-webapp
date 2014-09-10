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
        device = models.Devices(
            nome=self.request.params.get('nome'),
            obs=self.request.params.get('obs')
            )
        device.save()

        self.response.status = 201

    def put(self):
        pk = self.request.params.get('id')
        device = models.Devices.get_by_id(pk)

        if not device:
            self.abort(404)

        device['nome'] = self.request.params.get('nome')
        device['obs'] = self.request.params.get('obs')
        device.save()

        self.response.status = 204

    def delete(self):
        pk = self.request.params.get('id')
        device = models.Devices.get_by_id(pk)

        if not device:
            self.abort(404)

        device.delete()

        self.response.status = 204


class DeviceMedidasHandler(webapp2.RequestHandler):
    def get(self, device_id):
        device = models.Devices.get_by_id(device_id)

        if not device:
            self.abort(404)

        device['medidas'] = device.medidas()

        self.response.content_type = 'application/json'
        self.response.write(json.dumps(device))


    def post(self, device_id):
        device = models.Devices.get_by_id(device_id)

        if not device:
            self.abort(404)

        medida = models.Medidas(
            device_id=device_id,
            temperatura=self.request.params.get('temperatura'),
            humidade=self.request.params.get('humidade'),
            lat=self.request.params.get('lat'),
            lng=self.request.params.get('lng')
        )

        medida.save()

        self.response.status = 204

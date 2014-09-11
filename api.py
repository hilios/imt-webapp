import json
import webapp2
import sqlite3
import models

class DevicesHandler(webapp2.RequestHandler):
    def get(self):
        'Retorna todos os devices registrados'
        devices = models.Devices.get_all()

        self.response.content_type = 'application/json'
        self.response.write(json.dumps(devices))

    def post(self):
        'Cria um novo device, parametros: nome, obs'
        device = models.Devices(
            nome=self.request.params.get('nome'),
            obs=self.request.params.get('obs')
            )
        device.save()

        self.response.status = 201

    def put(self):
        'Atualiza um device, parametros: id, nome, obs'
        pk = self.request.params.get('id')
        device = models.Devices.get_by_id(pk)

        if not device:
            self.abort(404)

        device['nome'] = self.request.params.get('nome')
        device['obs'] = self.request.params.get('obs')
        device.save()

        self.response.status = 204

    def delete(self):
        'Deleta um device'
        pk = self.request.params.get('id')
        device = models.Devices.get_by_id(pk)

        if not device:
            self.abort(404)

        device.delete()

        self.response.status = 204


class MedidasDeviceHandler(webapp2.RequestHandler):
    def get(self, device_id):
        'Retorna um device com todas as medidas coletadas'
        device = models.Devices.get_by_id(device_id)

        if not device:
            self.abort(404)

        device['medidas'] = device.medidas()

        self.response.content_type = 'application/json'
        self.response.write(json.dumps(device))


    def post(self, device_id):
        '''Cria uma nova medida para um device, parametros: temperatura,
        humidade, lat, lng
        '''
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

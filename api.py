import json
import webapp2

from helpers import db
from datetime import datetime


class DevicesHandler(webapp2.RequestHandler):
    def get(self):
        'Retorna todos os devices registrados'
        with db.connection() as conn:
            query = conn.execute('SELECT * FROM devices')
            devices = query.fetchall()

        self.response.content_type = 'application/json'
        self.response.out.write(json.dumps(devices))

    def post(self):
        'Cria um novo device'
        with db.connection() as conn:
            query = conn.execute("""INSERT INTO devices (nome)
            VALUES (?)
            """, (
                self.request.params.get('nome'),
            ))

        self.response.status = 201

    def put(self):
        if not self.request.params.get('id'):
            self.abort(404)

        with db.connection() as conn:
            query = conn.execute("""UPDATE devices
            SET nome=?
            WHERE id=?
            """, (
                self.request.params.get('nome'),
                self.request.params.get('id'),
            ))

        self.response.status = 204

    def delete(self):
        if not self.request.params.get('id'):
            self.abort(404)

        with db.connection() as conn:
            query = conn.execute("""DELETE FROM devices
            WHERE id=?
            """, (
                self.request.params.get('id'),
            ))

        self.response.status = 204


class DeviceDataHandler(webapp2.RequestHandler):
    def get(self, device_id=None):
        limit = self.request.params.get('limit', 1)

        with db.connection() as conn:
            device = conn.execute("SELECT * FROM devices WHERE id=?",
                device_id)
            device = device.fetchone()

            if not device:
                self.abort(404)

            data = conn.execute("""SELECT * from device_data
            WHERE device_id=?
            ORDER BY recebido_em ASC
            LIMIT ?
            """, (device_id, limit))

            data = data.fetchall()

            # Adiciona a data ao objecto do device
            device['data'] = data

        self.response.content_type = 'application/json'
        self.response.out.write(json.dumps(device))

    def post(self, device_id=None):
        with db.connection() as conn:
            device = conn.execute("SELECT * FROM devices WHERE id=?",
                device_id)
            device = device.fetchone()

            if not device:
                self.abort(404)

            data = conn.execute("""INSERT INTO device_data (
                device_id,
                recebido_em,
                temperatura,
                lat,
                lng
            )
            VALUES (?, ?, ?, ?, ?)
            """, (
                device_id,
                datetime.now(),
                self.request.params.get('temperatura'),
                self.request.params.get('lat'),
                self.request.params.get('lng'),
            ))

        self.response.status = 204

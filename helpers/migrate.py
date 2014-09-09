#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import db
from datetime import timedelta
from datetime import datetime as date
from random import uniform as random


print """
 ___   ___       __    ____  _      ____  ___    __   _____  ___   ___
| |_) | | \     / /`_ | |_  | |\ | | |_  | |_)  / /\   | |  / / \ | |_)
|_|_) |_|_/     \_\_/ |_|__ |_| \| |_|__ |_| \ /_/--\  |_|  \_\_/ |_| \\
________________________________________________________________________
"""

if os.path.exists(db.DB_PATH):

    renew = raw_input('A Base de dados já existe, ' +
        'você deseja criar ela novamente? [Sn] ')

    if re.match('S', renew, re.I):
        os.remove(db.DB_PATH)
    else:
        print ""
        os.abort()

# Start migration
with db.Connection() as conn:
    print 'Criando tabelas...'
    # Create all tables
    conn.executescript("""CREATE TABLE devices (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        nome    TEXT
    );

    CREATE TABLE device_data (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id   INT NOT NULL,
        recebido_em INT NOT NULL,
        temperatura INT NOT NULL,
        lat         INT,
        lng         INT,

        FOREIGN KEY(device_id) REFERENCES devices(id)  ON DELETE CASCADE
    );

    CREATE INDEX datadeviceid ON device_data(device_id);
    """)

    print '\t> `devices`'
    print '\t> `device_data`'

print ''
fixtures = raw_input('Quer incluir dados fictícios para teste? [Sn] ')

if re.match(r'S', fixtures, re.I):
    with db.Connection() as conn:
        print 'Criando um `device`...'
        conn.execute("INSERT INTO devices (nome) VALUES ('DEF-1234')")


        device_id = conn.lastrowid
        print '\t> Device ID #%s criado!' % device_id

        print ''
        print 'Criando dados para este `device`:'

        print '\t+{:-^60}+'.format('')
        print '\t| {:<14}| {:<22}| {:<18} |'.format('Temperatura', 'Data', 'GIS')
        print '\t+{:-^60}+'.format('')

        for i in range(10):
            t = random(-2, 5)
            d = date.utcnow() - timedelta(random(0, -2))
            lat = -23.648241 + random(-1, 1)
            lng = -46.573678 + random(-1, 1)

            print '\t| {:+.2f}ºC' \
                '\t| {:%d/%m/%y %H:%M:%S}' \
                '\t| @{:+.4f},{:+.4f} |'.format(t, d, lat, lng)

            conn.execute("""INSERT INTO device_data
            (device_id, recebido_em, temperatura, lat, lng) VALUES
            (?, ?, ?, ?, ?);
            """, (device_id, d, t, lat, lng))

        print '\t+{:-^60}+'.format('')

print ''
print 'Banco de dados incializado com sucesso!'

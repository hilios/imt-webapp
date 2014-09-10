#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import models
from datetime import timedelta
from datetime import datetime as date
from random import uniform as random


print """
 ___   ___       __    ____  _      ____  ___    __   _____  ___   ___
| |_) | | \     / /`_ | |_  | |\ | | |_  | |_)  / /\   | |  / / \ | |_)
|_|_) |_|_/     \_\_/ |_|__ |_| \| |_|__ |_| \ /_/--\  |_|  \_\_/ |_| \\
________________________________________________________________________
"""

if os.path.exists(models.DB_PATH):

    renew = raw_input('A Base de dados já existe, ' +
        'você deseja criar ela novamente? [Sn] ')

    if re.match('S', renew, re.I):
        os.remove(models.DB_PATH)
    else:
        exit()

# Start migration
with models.dbconnection() as conn:
    print 'Criando tabelas...'
    # Create all tables
    conn.executescript("""CREATE TABLE devices (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        nome    TEXT
    );

    CREATE TABLE measures (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id   INT NOT NULL,
        recebido_em INT NOT NULL,
        temperatura INT NOT NULL,
        humidade    INT NOT NULL,
        lat         INT,
        lng         INT,

        FOREIGN KEY(device_id) REFERENCES devices(id)  ON DELETE CASCADE
    );

    CREATE INDEX measures__device_id ON measures(device_id);
    """)

    print '\t> `devices`'
    print '\t> `measures`'

print ''
fixtures = raw_input('Quer incluir dados fictícios para teste? [Sn] ')

if re.match(r'S', fixtures, re.I):
    print 'Criando um `device`...'

    device = models.Devices(nome='DEF-1234')
    device.save()

    print (''
        + '\t+{:-^25}+\n'
        + '\t| {:^5} | {:^15} |\n'
        + '\t+{:-^25}+'
    ).format('', 'id', 'Nome', '')
    print '\t| {id:^5} | {nome:<15} |'.format(**device)
    print '\t+{:-^25}+\n'.format('')

    print 'Criando dados para o `device` #{}:'.format(device['id'])

    print (''
        + '\t+{:-^80}+\n'
        + '\t| {:^5} | {:^18} | {:^15} | {:^10} | {:^20} |\n'
        + '\t+{:-^80}+'
    ).format('', 'id', 'Data', 'Temperatura',
            'Humidade', 'Posição', '')

    for i in range(15):
        t = random(-2, 5)
        h = random(0.0, 1.0)
        d = date.utcnow() - timedelta(random(0, -2))
        lat = -23.648241 + random(-1, 1)
        lng = -46.573678 + random(-1, 1)

        measure = models.Measures(
            device_id=device.get('id'),
            temperatura=t,
            humidade=h,
            recebido_em=d,
            lat=lat,
            lng=lng
        )
        measure.save()

        print (''
            + '\t'
            + '| {id:^5} '
            + '| {recebido_em:%d/%m/%y %H:%M:%S}  '
            + '| {temperatura:<15}  '
            + '| {humidade:<10} '
            + '| {gis:<15} '
            + '|'
        ).format(
            id=measure['id'],
            recebido_em=measure['recebido_em'],
            humidade='{humidade:0.1%}'.format(**measure),
            temperatura='{temperatura:+.2f}ºC'.format(**measure),
            gis='@{lat:+.4f},{lng:+.4f}'.format(**measure)
        )

    print '\t+{:-^80}+'.format('')

print ''
print 'Banco de dados incializado com sucesso!'

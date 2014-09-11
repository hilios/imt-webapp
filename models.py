import os
import sqlite3

from datetime import datetime


DB_FILE = 'db.sqlite3' # :memory:
DB_PATH = os.path.join(os.getcwd(), DB_FILE)


class dbconnection:
    def dict_factory(self, cursor, row):
        """Converte o resultado do consulta em um dicionario sendo a chave o
        nome da coluna."""
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def __enter__(self):
        self.dbconn = sqlite3.connect(DB_PATH)
        self.dbconn.row_factory = self.dict_factory

        return self.dbconn.cursor()

    def __exit__(self, type, value, traceback):
        self.dbconn.commit()
        self.dbconn.close()


class Model(dict):

    pk='id'
    table = None

    @classmethod
    def count(cls):
        with dbconnection() as conn:
            query = conn.execute('SELECT COUNT({pk}) AS count FROM {table}'\
                .format(table=cls.table, pk=cls.pk))
            result = query.fetchone()

        return int(result['count'])

    @classmethod
    def get_all(cls):
        with dbconnection() as conn:
            query = conn.execute('SELECT * FROM {table}'\
                .format(table=cls.table))
            result = query.fetchall()

        return map(cls, result)

    @classmethod
    def get_by_id(cls, pk):
        with dbconnection() as conn:
            query = conn.execute('SELECT * FROM {table} WHERE {pk}=?'\
                .format(table=cls.table, pk=cls.pk), (pk,))
            result = query.fetchone()

        if result:
            return cls(result)

        return None

    @classmethod
    def get_by(cls, **kwargs):
        with dbconnection() as conn:
            where = ' AND '.join(['{0}=:{0}'.format(col)
                for col, val in kwargs.items()])

            query = conn.execute('SELECT * FROM {table} WHERE {where}'\
                .format(table=cls.table, where=where), kwargs)
            result = query.fetchall()

        return map(cls, result)

    def _insert(self):
        values = ','.join([':{}'.format(key) for key in self.keys()])
        columns = ','.join(self.keys())

        with dbconnection() as conn:
            query = conn.execute('''INSERT INTO {table}
            ({columns}) VALUES ({values})'''\
            .format(columns=columns, values=values, table=self.table),
            self)

            return conn.lastrowid

    def _update(self):
        setter = ','.join(['{0}=:{0}'.format(col)
            for col, val in self.items() if not col == self.pk])

        with dbconnection() as conn:
            query = conn.execute('''UPDATE OR ROLLBACK devices
            SET {setter} WHERE {pk}=:id'''\
            .format(setter=setter, pk=self.pk), self)

    def save(self):
        if not self.has_key(self.pk):
            pk = self._insert()
            self[self.pk] = pk
        else:
            self._update()

        return True

    def delete(self):
        with dbconnection() as conn:
            query = conn.execute('DELETE FROM {table} WHERE {pk}=:id'\
                .format(table=self.table, pk=self.pk), self)

        return True

    def to_dict(self):
        return self


class Devices(Model):
    table = 'devices'

    def medidas(self):
        pk = self.get('id', 0)
        return Medidas.get_by(device_id=pk)


class Medidas(Model):
    table = 'medidas'

    def _insert(self):
        self['recebido_em'] = datetime.utcnow()
        return super(Medidas, self)._insert()

import os
import sqlite3


DB_FILE = 'db.sqlite3' # :memory:
DB_PATH = os.path.join(os.getcwd(), DB_FILE)


class connection:
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

import sqlite3
from config import DATABASE_FILE_PATH


class Database:
    def __init__(self, db_path=DATABASE_FILE_PATH, connection=None):
        self._db_path = db_path
        self._injected_connection = connection

    def get_connection(self):
        if self._injected_connection is not None:
            return self._injected_connection

        con = sqlite3.connect(self._db_path)
        con.execute("PRAGMA foreign_keys = ON")
        con.row_factory = sqlite3.Row
        return con

    def execute(self, sql, params=None):
        if params is None:
            params = []

        con = self.get_connection()
        result = con.execute(sql, params)

        if self._injected_connection is None:
            con.commit()
            con.close()

        return result.lastrowid

    def query(self, sql, params=None):
        if params is None:
            params = []

        con = self.get_connection()
        result = con.execute(sql, params).fetchall()

        if self._injected_connection is None:
            con.close()

        return result

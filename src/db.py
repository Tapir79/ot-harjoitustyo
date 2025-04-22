import sqlite3
from config import DATABASE_FILE_PATH

_connection = None


def set_connection(conn):
    global _connection
    _connection = conn


def get_connection():
    global _connection
    if _connection is not None:
        return _connection  # use injected test connection

    con = sqlite3.connect(DATABASE_FILE_PATH)
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con


def execute(sql, params=None):
    if params is None:
        params = []
    con = get_connection()
    result = con.execute(sql, params)
    if _connection is None:
        con.commit()
        con.close()
    return result.lastrowid


def query(sql, params=None):
    if params is None:
        params = []
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    if _connection is None:
        con.close()
    return result

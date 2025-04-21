import sqlite3
from config import DATABASE_FILE_PATH


def get_connection():
    con = sqlite3.connect(DATABASE_FILE_PATH)
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con


def execute(sql, params=None):
    if params is None:
        params = []
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    con.close()
    return result.lastrowid


def query(sql, params=None):
    if params is None:
        params = []
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    con.close()
    return result

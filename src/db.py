import sqlite3
from config import DATABASE_FILE_PATH


class Database:
    """
    A database helper class for handling SQL connection, queries
    and statements to the database. 
    """

    def __init__(self, db_path=DATABASE_FILE_PATH, connection=None):
        """
        Initialize the Database object.

        Args:
            db_path (str): Path to the SQLite database file.
            connection (sqlite3.Connection, optional): 
            Injected connection to be able to use any db in testing.
        """
        self._db_path = db_path
        self._injected_connection = connection

    def get_connection(self):
        """
        Get a database connection.
        Uses an injected connection if provided, otherwise opens a new one.

        Returns:
            sqlite3.Connection: A database connection.
        """
        if self._injected_connection is not None:
            return self._injected_connection

        con = sqlite3.connect(self._db_path)
        con.execute("PRAGMA foreign_keys = ON")
        con.row_factory = sqlite3.Row
        return con

    def execute(self, sql, params=None):
        """
        Execute an INSERT, UPDATE, or DELETE statement.

        Args:
            sql (str): The SQL statement to execute.
            params (list, optional): Parameters to bind to the statement.

        Returns:
            int: The last inserted row ID.
        """
        if params is None:
            params = []

        con = self.get_connection()
        result = con.execute(sql, params)

        if self._injected_connection is None:
            con.commit()
            con.close()

        return result.lastrowid

    def query(self, sql, params=None):
        """
        Execute a SELECT query and fetch all results.

        Args:
            sql (str): The SQL query to execute.
            params (list, optional): Parameters to bind to the query.

        Returns:
            list: A list of rows from the result set.
        """
        if params is None:
            params = []

        con = self.get_connection()
        result = con.execute(sql, params).fetchall()

        if self._injected_connection is None:
            con.close()

        return result

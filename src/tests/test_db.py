import unittest
from unittest.mock import patch, MagicMock
import db
from db import Database
import sqlite3


class TestGetConnectionWithMock(unittest.TestCase):
    @patch("db.sqlite3.connect")
    def test_get_connection_sets_foreign_keys_and_row_factory(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        db_instance = Database()
        conn = db_instance.get_connection()
        mock_connect.assert_called_once()
        mock_conn.execute.assert_called_with("PRAGMA foreign_keys = ON")

        self.assertEqual(mock_conn.row_factory, sqlite3.Row)
        self.assertEqual(conn, mock_conn)

    @patch("db.sqlite3.connect")
    def test_none_execute_params_does_not_return_id(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        db_instance = Database()
        result = db_instance.execute("", None)
        self.assertIsNotNone(result)

    @patch("db.sqlite3.connect")
    def test_none_query_params_does_not_return_id(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        mock_conn.execute.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db_instance = Database()
        result = db_instance.query("", None)
        self.assertEqual(result, [])

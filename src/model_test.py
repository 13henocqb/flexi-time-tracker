import unittest
import sqlite3
import tempfile
import shutil
import os

from model import DatabaseHandler

class TestDatabaseHandler(unittest.TestCase):
    def setUp(self):
        self.temp_folder = tempfile.mkdtemp()
        db_path = os.path.join(self.temp_folder, "test_db.sqlite")
        self.db_handler = DatabaseHandler(db_path)

    def tearDown(self):
        self.db_handler.close()
        if os.path.exists(self.temp_folder):
            shutil.rmtree(self.temp_folder)

    def test_create_table_success(self):
        table_name = "test_table"
        attributes = {"id":"INTEGER PRIMARY KEY", "first_name":"TEXT", "last_name":"TEXT"}
        self.db_handler.create_table(table_name, attributes)
        tables, error = self.db_handler.query_data("SELECT name FROM sqlite_master WHERE type='table'")
        self.assertIsNone(error)
        table_names = [table["name"] for table in tables]
        self.assertIn(table_name, table_names)

    def test_insert_and_get_data_success(self):
        table_name = "test_table"
        attributes = {"id":"INTEGER PRIMARY KEY", "first_name":"TEXT", "last_name":"TEXT"}
        self.db_handler.create_table(table_name, attributes)
        data = ["John", "Doe"]
        self.db_handler.insert_data(table_name, data)
        result, error = self.db_handler.get_data(["first_name", "last_name"], table_name)
        self.assertIsNone(error)
        self.assertEqual(result, [{"first_name": "John", "last_name" : "Doe"}])

    def test_update_data_success(self):
        table_name = "test_table"
        attributes = {"id":"INTEGER PRIMARY KEY", "first_name":"TEXT", "last_name":"TEXT"}
        self.db_handler.create_table(table_name, attributes)
        data = ["John", "Doe"]
        id, error = self.db_handler.insert_data(table_name, data)
        self.assertIsNone(error)
        self.db_handler.update_data(table_name, {"last_name": "Smith"}, id)
        result, error = self.db_handler.get_data(["last_name"], table_name, [f"id == {id}"])
        self.assertIsNone(error)
        self.assertEqual(result, [{"last_name": "Smith"}])
            
    def test_delete_row_success(self):
        table_name = "test_table"
        attributes = {"id":"INTEGER PRIMARY KEY", "first_name":"TEXT", "last_name":"TEXT"}
        self.db_handler.create_table(table_name, attributes)
        data = ["John", "Doe"]
        id, error = self.db_handler.insert_data(table_name, data)
        self.assertIsNone(error)
        self.db_handler.delete_row(table_name, f"id = {id}")
        result, error = self.db_handler.get_data(["first_name", "last_name"], table_name)
        self.assertIsNone(error)
        self.assertEqual(result, [])

    def test_delete_table_success(self):
        table_name = "test_table"
        attributes = {"id":"INTEGER PRIMARY KEY", "first_name":"TEXT", "last_name":"TEXT"}
        self.db_handler.create_table(table_name, attributes)
        self.db_handler.delete_table(table_name)
        tables, error = self.db_handler.query_data("SELECT name FROM sqlite_master WHERE type='table'")
        self.assertIsNone(error)
        table_names = [table["name"] for table in tables]
        self.assertNotIn(table_name, table_names)

    def test_create_table_empty_name(self):
        attributes = {"id": "INTEGER PRIMARY KEY", "first_name": "TEXT", "last_name": "TEXT"}
        error = self.db_handler.create_table("", attributes)
        self.assertIsInstance(error, sqlite3.Error)

    def test_insert_data_empty_table_name(self):
        data = ["John", "Doe"]
        result, error = self.db_handler.insert_data("", data)
        self.assertIsInstance(error, sqlite3.Error)

    def test_get_data_nonexistent_table(self):
        result, error = self.db_handler.get_data(["first_name", "last_name"], "nonexistent_table")
        self.assertIsInstance(error, sqlite3.Error)

    def test_query_data_nonexistent_table(self):
        result, error = self.db_handler.query_data("SELECT * FROM nonexistent_table")
        self.assertIsInstance(error, sqlite3.Error)

    def test_delete_table_empty_name(self):
        error = self.db_handler.delete_table("")
        self.assertIsInstance(error, sqlite3.Error)

    def test_update_data_invalid_column(self):
        table_name = "test_table"
        attributes = {"id": "INTEGER PRIMARY KEY", "first_name": "TEXT", "last_name": "TEXT"}
        self.db_handler.create_table(table_name, attributes)
        data = ["John", "Doe"]
        id, error = self.db_handler.insert_data(table_name, data)
        error = self.db_handler.update_data(table_name, {"last_name": "Smith"}, {"invalid_column": id})
        self.assertIsInstance(error, sqlite3.Error)

    def test_delete_row_invalid_column(self):
        table_name = "test_table"
        attributes = {"id": "INTEGER PRIMARY KEY", "first_name": "TEXT", "last_name": "TEXT"}
        self.db_handler.create_table(table_name, attributes)
        data = ["John", "Doe"]
        id, error = self.db_handler.insert_data(table_name, data)
        error = self.db_handler.delete_row(table_name, f"invalid_column = {id}")
        self.assertIsInstance(error, sqlite3.Error)

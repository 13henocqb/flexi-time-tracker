import unittest
import sqlite3
import os

from model import DatabaseHandler

class TestDatabaseHandler(unittest.TestCase):
    def setUp(self):
        self.db_path = 'test_db.sqlite'
        self.db_handler = DatabaseHandler(self.db_path)

    def tearDown(self):
        self.db_handler.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_create_table(self):
        table_name = 'test_table'
        columns = {'id':'INTEGER PRIMARY KEY', 'first_name':'TEXT', 'last_name':'TEXT'}
        self.db_handler.create_table(table_name, columns)
        
        tables = self.db_handler.query_data("SELECT name FROM sqlite_master WHERE type='table'")
        table_names = [table['name'] for table in tables]
        self.assertIn(table_name, table_names)

    def test_insert_and_get_data(self):
        table_name = 'test_table'
        columns = {'id':'INTEGER PRIMARY KEY', 'first_name':'TEXT', 'last_name':'TEXT'}
        self.db_handler.create_table(table_name, columns)
        data = ('John', 'Doe')
        self.db_handler.insert_data(table_name, data)

        result = self.db_handler.get_data(['first_name', 'last_name'], table_name)
        self.assertEqual(result, [{'first_name': 'John', 'last_name' : 'Doe'}])

    def test_update_data(self):
        table_name = 'test_table'
        columns = {'id':'INTEGER PRIMARY KEY', 'first_name':'TEXT', 'last_name':'TEXT'}
        self.db_handler.create_table(table_name, columns)
        data = ('John', 'Doe')
        id = self.db_handler.insert_data(table_name, data)

        self.db_handler.update_data(table_name, {'last_name': 'Smith'}, id)
        result = self.db_handler.get_data(['last_name'], table_name, [f'id == {id}'])
        self.assertEqual(result, [{'last_name': 'Smith'}])
            
    def test_delete_row(self):
        table_name = 'test_table'
        columns = {'id':'INTEGER PRIMARY KEY', 'first_name':'TEXT', 'last_name':'TEXT'}
        self.db_handler.create_table(table_name, columns)
        data = ('John', 'Doe')
        id = self.db_handler.insert_data(table_name, data)

        self.db_handler.delete_row(table_name, f'id = {id}')
        result = self.db_handler.get_data(['first_name', 'last_name'], table_name)
        self.assertEqual(result, [])

    def test_delete_table(self):
        table_name = 'test_table'
        columns = {'id':'INTEGER PRIMARY KEY', 'first_name':'TEXT', 'last_name':'TEXT'}
        self.db_handler.create_table(table_name, columns)

        self.db_handler.delete_table(table_name)
        tables = self.db_handler.query_data("SELECT name FROM sqlite_master WHERE type='table'")
        table_names = [table['name'] for table in tables]
        self.assertNotIn(table_name, table_names)

if __name__ == '__main__':
    unittest.main()

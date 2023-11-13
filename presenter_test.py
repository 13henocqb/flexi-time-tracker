import unittest
import sqlite3
import os

from presenter import UserHandler, TimesheetHandler
from model import DatabaseHandler

class TestUserHandler(unittest.TestCase):
    def setUp(self):
        self.db_path = 'test_db.sqlite'
        self.db_handler = DatabaseHandler(self.db_path)
        self.user_handler = UserHandler(self.db_handler)

    def tearDown(self):
        self.db_handler.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_create_user(self):
        user_id = self.user_handler.create_user("Colin Baker", "six@example.com", "password123", "IT", "User")
        self.assertIsNotNone(user_id)

    def test_get_user_by_id(self):
        user_id = self.user_handler.create_user("Sylvester McCoy", "seven@example.com", "pass456", "HR", "Manager")
        user = self.user_handler.get_user_by_id(user_id)
        self.assertIsNotNone(user)
        self.assertEqual(user.name, "Sylvester McCoy")

    def test_authenticate_user(self):
        self.user_handler.create_user("Paul McGann", "eight@example.com", "secure789", "Finance", "User")
        authenticated_user = self.user_handler.authenticate_user("eight@example.com", "secure789")
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user.name, "Paul McGann")

class TestTimesheetHandler(unittest.TestCase):
    def setUp(self):
        self.db_path = 'test_db.sqlite'
        self.db_handler = DatabaseHandler(self.db_path)
        self.user_handler = UserHandler(self.db_handler)
        self.timesheet_handler = TimesheetHandler(self.db_handler)

    def tearDown(self):
        self.db_handler.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_create_timesheet(self):
        user_id = self.user_handler.create_user("William Hartnell", "one@example.com", "password123", "IT", "User")
        timesheet_id = self.timesheet_handler.create_timesheet(user_id, "IT", "Pending")
        self.assertIsNotNone(timesheet_id)

    def test_get_timesheet_by_id(self):
        user_id = self.user_handler.create_user("Patrick Troughton", "two@example.com", "pass456", "HR", "Manager")
        timesheet_id = self.timesheet_handler.create_timesheet(user_id, "HR", "Approved")
        timesheet = self.timesheet_handler.get_timesheet_by_id(timesheet_id)
        self.assertIsNotNone(timesheet)
        self.assertEqual(timesheet.department, "HR")

    def test_set_timesheet_status(self):
        user_id = self.user_handler.create_user("Jon Pertwee", "three@example.com", "secure789", "Finance", "User")
        timesheet_id = self.timesheet_handler.create_timesheet(user_id, "Finance", "Pending")
        self.timesheet_handler.set_timesheet_status(timesheet_id, "Approved")
        timesheet = self.timesheet_handler.get_timesheet_by_id(timesheet_id)
        self.assertEqual(timesheet.status, "Approved")

    def test_create_timesheet_entry(self):
        user_id = self.user_handler.create_user("Tom Baker", "four@example.com", "pass789", "Sales", "User")
        timesheet_id = self.timesheet_handler.create_timesheet(user_id, "Sales", "Pending")
        self.timesheet_handler.create_timesheet_entry(timesheet_id, "2023-01-01", 8.5)
        entries = self.timesheet_handler.get_entries_by_timesheet_id(timesheet_id)
        self.assertEqual(len(entries), 1)

    def test_get_flexi_balance(self):
        user_id = self.user_handler.create_user("Peter Davison", "five@example.com", "pass123", "Marketing", "User")
        timesheet_id = self.timesheet_handler.create_timesheet(user_id, "Marketing", "Approved")
        self.timesheet_handler.create_timesheet_entry(timesheet_id, "2023-01-01", 5.5)
        self.timesheet_handler.create_timesheet_entry(timesheet_id, "2023-01-02", 14.5)
        balance = self.timesheet_handler.get_flexi_balance(user_id, daily_expected_hours=10)
        self.assertEqual(balance, 0)

if __name__ == '__main__':
    unittest.main()
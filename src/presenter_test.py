import unittest
import tempfile
import os
import shutil

from presenter import UserHandler, TimesheetHandler
from model import DatabaseHandler

class TestUserHandler(unittest.TestCase):
    def setUp(self):
        self.temp_folder = tempfile.mkdtemp()
        db_path = os.path.join(self.temp_folder, "test_db.sqlite")
        self.db_handler = DatabaseHandler(db_path)
        self.user_handler = UserHandler(self.db_handler)

    def tearDown(self):
        self.db_handler.close()
        if os.path.exists(self.temp_folder):
            shutil.rmtree(self.temp_folder)

    def test_create_user_success(self):
        user_id = self.user_handler.create_user("Christopher Eccleston", "nine@example.com", "password123", "IT", "User")
        self.assertIsNotNone(user_id)

    def test_get_user_by_id_success(self):
        user_id = self.user_handler.create_user("David Tennant", "ten@example.com", "pass456", "HR", "Manager")
        user = self.user_handler.get_user_by_id(user_id)
        self.assertIsNotNone(user)
        self.assertEqual(user.name, "David Tennant")

    def test_authenticate_user_success(self):
        self.user_handler.create_user("Matt Smith", "eleven@example.com", "secure789", "Finance", "User")
        authenticated_user = self.user_handler.authenticate_user("eleven@example.com", "secure789")
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user.name, "Matt Smith")

    def test_authenticate_user_invalid_password(self):
        self.user_handler.create_user("Peter Capaldi", "twelve@example.com", "valid_password", "IT", "User")
        user = self.user_handler.authenticate_user("twelve@example.com", "invalid_password")
        self.assertIsNone(user)

    def test_get_user_by_id_not_found(self):
        user_id = 9999 
        user = self.user_handler.get_user_by_id(user_id)
        self.assertIsNone(user)

    def test_create_user_empty_name(self):
        user_id = self.user_handler.create_user("", "empty_name@example.com", "password123", "IT", "User")
        self.assertIsNotNone(user_id)

    def test_create_user_max_length(self):
        user_id = self.user_handler.create_user("A" * 255, "max_length@example.com", "password123", "IT", "User")
        self.assertIsNotNone(user_id)

    def test_create_user_duplicate_emails(self):
        user_id_1 = self.user_handler.create_user("Rowan Atkinson", "nine@example.com", "password123", "IT", "User")
        user_id_2 = self.user_handler.create_user("Richard E Grant", "nine@example.com", "password123", "IT", "User")
        self.assertNotEqual(user_id_1, user_id_2)

    def test_authenticate_user_empty_fields(self):
        authenticated_user_empty = self.user_handler.authenticate_user("", "")
        self.assertIsNone(authenticated_user_empty)

    def test_authenticate_user_invalid_email(self):
        authenticated_user_invalid_email = self.user_handler.authenticate_user("invalidemail", "password123")
        self.assertIsNone(authenticated_user_invalid_email)

class TestTimesheetHandler(unittest.TestCase):
    def setUp(self):
        self.temp_folder = tempfile.mkdtemp()
        db_path = os.path.join(self.temp_folder, "test_db.sqlite")
        self.db_handler = DatabaseHandler(db_path)
        self.user_handler = UserHandler(self.db_handler)
        self.timesheet_handler = TimesheetHandler(self.db_handler)

    def tearDown(self):
        self.db_handler.close()
        if os.path.exists(self.temp_folder):
            shutil.rmtree(self.temp_folder)

    def test_create_timesheet_success(self):
        user_id = self.user_handler.create_user("William Hartnell", "one@example.com", "password123", "IT", "User")
        timesheet_id = self.timesheet_handler.create_timesheet(user_id, "IT", "Pending")
        self.assertIsNotNone(timesheet_id)

    def test_get_timesheet_by_id_success(self):
        user_id = self.user_handler.create_user("Patrick Troughton", "two@example.com", "pass456", "HR", "Manager")
        timesheet_id = self.timesheet_handler.create_timesheet(user_id, "HR", "Approved")
        timesheet = self.timesheet_handler.get_timesheet_by_id(timesheet_id)
        self.assertIsNotNone(timesheet)
        self.assertEqual(timesheet.department, "HR")

    def test_get_timesheets_by_status_success(self):
        user_id_1 = self.user_handler.create_user("Jon Pertwee", "three@example.com", "secure789", "IT", "User")
        self.timesheet_handler.create_timesheet(user_id_1, "IT", "Pending")

        user_id_2 = self.user_handler.create_user("Tom Baker", "four@example.com", "pass789", "HR", "User")
        self.timesheet_handler.create_timesheet(user_id_2, "HR", "Approved")

        user_id_3 = self.user_handler.create_user("Peter Davison", "five@example.com", "pass123", "Finance", "User")
        self.timesheet_handler.create_timesheet(user_id_3, "Finance", "Pending")

        timesheets_pending_it = self.timesheet_handler.get_timesheets_by_status("IT", "Pending")
        timesheets_approved_hr = self.timesheet_handler.get_timesheets_by_status("HR", "Approved")
        timesheets_pending_finance = self.timesheet_handler.get_timesheets_by_status("Finance", "Pending")

        self.assertEqual(len(timesheets_pending_it), 1)
        self.assertEqual(len(timesheets_approved_hr), 1)
        self.assertEqual(len(timesheets_pending_finance), 1)

        self.assertEqual(timesheets_pending_it[0].department, "IT")
        self.assertEqual(timesheets_approved_hr[0].status, "Approved")
        self.assertEqual(timesheets_pending_finance[0].employee_id, user_id_3)

    def test_set_timesheet_status_success(self):
        user_id = self.user_handler.create_user("Colin Baker", "six@example.com", "pass234", "IT", "User")
        timesheet_id = self.timesheet_handler.create_timesheet(user_id, "Finance", "Pending")
        self.timesheet_handler.set_timesheet_status(timesheet_id, "Approved")
        timesheet = self.timesheet_handler.get_timesheet_by_id(timesheet_id)
        self.assertEqual(timesheet.status, "Approved")

    def test_create_timesheet_entry_success(self):
        user_id = self.user_handler.create_user("Sylvester McCoy", "seven@example.com", "pass567", "HR", "Manager")
        timesheet_id = self.timesheet_handler.create_timesheet(user_id, "Sales", "Pending")
        self.timesheet_handler.create_timesheet_entry(timesheet_id, "2023-01-01", 8.5)
        entries = self.timesheet_handler.get_entries_by_timesheet_id(timesheet_id)
        self.assertEqual(len(entries), 1)

    def test_get_flexi_balance_with_entries_success(self):
        user_id = self.user_handler.create_user("Paul McGann", "eight@example.com", "pass890", "Finance", "User")
        timesheet_id = self.timesheet_handler.create_timesheet(user_id, "Marketing", "Approved")
        self.timesheet_handler.create_timesheet_entry(timesheet_id, "2023-01-01", 5.5)
        self.timesheet_handler.create_timesheet_entry(timesheet_id, "2023-01-02", 15.5)
        balance = self.timesheet_handler.get_flexi_balance(user_id, daily_expected_hours=10)
        self.assertEqual(balance, 1)

    def test_get_timesheets_by_status_not_found(self):
        department = "NonexistentDepartment"
        status = "NonexistentStatus"
        timesheets = self.timesheet_handler.get_timesheets_by_status(department, status)
        self.assertIsNone(timesheets)

    def test_get_timesheet_by_id_not_found(self):
        timesheet_id = 9999  
        timesheets = self.timesheet_handler.get_timesheet_by_id(timesheet_id)
        self.assertIsNone(timesheets)
        
    def test_get_entries_by_timesheet_id_not_found(self):
        timesheet_id = 9999  
        entries = self.timesheet_handler.get_entries_by_timesheet_id(timesheet_id)
        self.assertEqual(entries, {})

    def test_get_flexi_balance_no_entries(self):
        user_id = 9999  
        balance = self.timesheet_handler.get_flexi_balance(user_id, daily_expected_hours=8)
        self.assertEqual(balance, 0)

    def test_set_timesheet_status_not_found(self):
        timesheet_id = 9999
        self.timesheet_handler.set_timesheet_status(timesheet_id, "Approved")
        timesheet = self.timesheet_handler.get_timesheet_by_id(timesheet_id)
        self.assertIsNone(timesheet)

    def test_create_timesheet_entry_min_max_values(self):
        user_id = self.user_handler.create_user("John Hurt", "war@example.com", "password123", "IT", "User")
        timesheet_id = self.timesheet_handler.create_timesheet(user_id, "IT", "Pending")
        entry_date_min_max = "2023-01-01"
        entry_hours_min_max = 24.0
        self.timesheet_handler.create_timesheet_entry(timesheet_id, entry_date_min_max, entry_hours_min_max)
        entries = self.timesheet_handler.get_entries_by_timesheet_id(timesheet_id)
        self.assertEqual(len(entries), 1)
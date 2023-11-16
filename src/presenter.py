from structures import User, Timesheet

class UserHandler:
    def __init__(self, db_handler):
        self.table_name = "users"
        table_attributes = {"user_id":"INTEGER PRIMARY KEY", "name":"TEXT", "email":"TEXT", "password":"TEXT", "department":"TEXT", "role":"TEXT"}

        self.db_handler = db_handler
        self.db_handler.create_table(self.table_name, table_attributes)

    def create_user(self, name, email, password, department, role):
        user_id, error = self.db_handler.insert_data(self.table_name, (name, email, password, department, role))
        return user_id

    def get_user_by_id(self, user_id):
        data =  ["*"]
        conditions = [f"user_id == {user_id}"]

        result, error = self.db_handler.get_data(data, self.table_name, conditions)
        
        if result:
            user = result[0] # Return the first matching record
            return User(user['user_id'], user['name'], user['email'], user['department'], 'User') 
        return None

    def authenticate_user(self, email, password):
        data =  ["*"]
        conditions = [f"email = '{email}'", f"password = '{password}'"]

        result, error = self.db_handler.get_data(data, self.table_name, conditions)
        
        if result:
            user = result[0] # Return the first matching record
            return User(user['user_id'], user['name'], user['email'], user['department'], user['role']) 
        return None

class TimesheetHandler:
    def __init__(self, db_handler):
        self.timesheet_table_name = "timesheets"
        self.timesheet_entry_table_name = "timesheet_entries"
        
        timesheet_table_attributes = {"timesheet_id":"INTEGER PRIMARY KEY", "user_id":"INTEGER", "department":"TEXT", "status":"TEXT"}
        timesheet_entry_table_attributes =  {"entry_id":"INTEGER PRIMARY KEY", "timesheet_id":"INTEGER", "date":"DATE", "hours_worked":"REAL"}
        
        self.db_handler = db_handler
        self.db_handler.create_table(self.timesheet_table_name, timesheet_table_attributes)
        self.db_handler.create_table(self.timesheet_entry_table_name, timesheet_entry_table_attributes)

    def create_timesheet(self, user_id, department, status):
        timesheet_id, error = self.db_handler.insert_data(self.timesheet_table_name, (user_id, department, status))
        return timesheet_id

    def get_timesheet_by_id(self, timesheet_id):
        data =  ["*"]
        conditions = [f"timesheet_id = {timesheet_id}"]

        result, error = self.db_handler.get_data(data, self.timesheet_table_name, conditions)

        if result:
            timesheet = result[0]
            worked_hours = self.get_entries_by_timesheet_id(timesheet["timesheet_id"])
            return Timesheet(timesheet["timesheet_id"], timesheet["user_id"], timesheet["department"], worked_hours, timesheet["status"])
        return None

    def get_timesheets_by_status(self, department, status):
        data =  ["*"]
        conditions = [f"department = '{department}'", f"status = '{status}'"]

        result, error = self.db_handler.get_data(data, self.timesheet_table_name, conditions)

        if result:
            timesheets = []

            for timesheet in result:
                worked_hours = self.get_entries_by_timesheet_id(timesheet["timesheet_id"])
                timesheets.append(Timesheet(timesheet["timesheet_id"], timesheet["user_id"], timesheet["department"], worked_hours, timesheet["status"]))

            return timesheets
        return None
    
    def set_timesheet_status(self, timesheet_id, status):
        data = {"status": status}
        condition = f"timesheet_id = {timesheet_id}"
        self.db_handler.update_data(self.timesheet_table_name, data, condition)

    def create_timesheet_entry(self, timesheet_id, date, hours_worked):
        self.db_handler.insert_data(self.timesheet_entry_table_name, (timesheet_id, date, hours_worked)) 

    def get_entries_by_timesheet_id(self, timesheet_id):
        data =  ["*"]
        conditions = [f"timesheet_id = {timesheet_id}"]

        timesheet_entries, error = self.db_handler.get_data(data, self.timesheet_entry_table_name, conditions)
        
        return {timesheet_entry["date"]: timesheet_entry["hours_worked"] for timesheet_entry in timesheet_entries}
    
    def get_flexi_balance(self, user_id, daily_expected_hours = 7.4):
        data =  ["hours_worked"]
        joins = {self.timesheet_table_name:"timesheet_id"}
        conditions = [f"user_id = {user_id}", "status != 'Denied'"]
        
        timesheet_entries, error = self.db_handler.get_data(data, self.timesheet_entry_table_name, conditions, joins)

        if timesheet_entries:
            total_worked_hours = sum(timesheet_entry['hours_worked'] for timesheet_entry in timesheet_entries)
            return total_worked_hours - (daily_expected_hours * len(timesheet_entries))
        else:
            return 0
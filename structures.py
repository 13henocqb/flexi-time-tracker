class User:
    def __init__(self, user_id, name, email, department, role):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.department = department
        self.role = role

class Timesheet:
    def __init__(self, timesheet_id, employee_id, department, worked_hours, status):
        self.timesheet_id = timesheet_id
        self.employee_id = employee_id
        self.department = department
        self.worked_hours = worked_hours
        self.status = status
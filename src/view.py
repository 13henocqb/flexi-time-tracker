import PySimpleGUI as sg
from datetime import datetime, timedelta

class FlexiTimeGUI:
    def __init__(self, user_handler, timesheet_handler, icon_path):
        self.user_handler = user_handler
        self.timesheet_handler = timesheet_handler
        self.icon_path = icon_path
        self.user = None
        
        sg.theme("LightGrey1")

    def main_page(self):
        layout = [
            [sg.Text("Welcome to the Flexi-Time App")],
            [sg.Text("Flexi Balance: ", key='-FLEXI_TEXT-', visible=False), 
                sg.Text("", key='-FLEXI_BALANCE-', visible=False)],
            [sg.Button("Log In", key="log_in")],
            [sg.Button("Create Timesheet", key="create_ts", disabled=True)],
            [sg.Button("View Timesheets", key="view_all_ts", visible=False)],
            [sg.Button("Exit")]
        ]

        main_window = sg.Window("Flexi-Time App", layout, icon=self.icon_path)

        while True:
            event, values = main_window.read()

            if event == sg.WIN_CLOSED or event == "Exit":
                break

            elif event == "log_in":
                self.user = self.login_page()

                if self.user != None:
                    main_window["log_in"].update(disabled=True)

                    if self.user.role == "Employee":
                        flexi_balance = self.timesheet_handler.get_flexi_balance(self.user.user_id)
                        main_window["-FLEXI_TEXT-"].update(visible=True)
                        main_window["-FLEXI_BALANCE-"].update(flexi_balance, visible=True)
                        main_window["create_ts"].update(disabled=False)

                    elif self.user.role == "Manager":
                        main_window["view_all_ts"].update(visible=True)

            elif event == "create_ts":
                if self.user != None:
                    self.create_timesheet_page()

            elif event == "view_all_ts":
                if self.user != None:
                    self.view_all_timesheets_page()

        main_window.close()

    def login_page(self):
        layout = [
            [sg.Text("Log In")],
            [sg.Text("Email:"), sg.InputText(key="email")],
            [sg.Text("Password:"), sg.InputText(key="password", password_char="*")],
            [sg.Button("Submit"), sg.Button("Exit")],
        ]

        login_window = sg.Window("Log In", layout, icon=self.icon_path)
        user = None

        while True:
            event, values = login_window.read()

            if event == sg.WIN_CLOSED or event == "Exit":
                break

            elif event == "Submit":
                email = values["email"]
                password = values["password"]

                user = self.user_handler.authenticate_user(email, password)
                
                if user == None:
                    sg.popup("Login Failed. Please check your credentials.", title="Error")
                else:
                    sg.popup("Login Successful", title="Success")
                    break

        login_window.close()
        return user

    def create_timesheet_page(self):
        layout = [
            [sg.Text("Create Timesheet")],
            [sg.Text("Start of the Week:"), sg.InputText(key="start_date"), 
                sg.CalendarButton("Select Date",close_when_date_chosen=True, target="start_date", format="%d-%m-%Y",size=(10,1))],
            [sg.Text("Hours Worked:")],
            [sg.Text("Monday:"), sg.InputText(key="monday")],
            [sg.Text("Tuesday:"), sg.InputText(key="tuesday")],
            [sg.Text("Wednesday:"), sg.InputText(key="wednesday")],
            [sg.Text("Thursday:"), sg.InputText(key="thursday")],
            [sg.Text("Friday:"), sg.InputText(key="friday")],
            [sg.Button("Submit Timesheet", key="submit_timesheet"), sg.Button("Exit")]
        ]

        create_timesheet_window = sg.Window("Create Timesheet", layout, icon=self.icon_path)

        while True:
            event, values = create_timesheet_window.read()

            if event == sg.WIN_CLOSED or event == "Exit":
                break

            elif event == "submit_timesheet":
                start_date = datetime.strptime(values["start_date"], "%d-%m-%Y")
                weeks_worked_hours =  [
                    values["monday"],
                    values["tuesday"],
                    values["wednesday"],
                    values["thursday"],
                    values["friday"]
                ]

                timesheet_id = self.timesheet_handler.create_timesheet(self.user.user_id, self.user.department, "Pending")

                for i, worked_hours in enumerate(weeks_worked_hours):
                    date = start_date + timedelta(days=i)

                    self.timesheet_handler.create_timesheet_entry(timesheet_id, date.strftime("%d-%m-%Y"), worked_hours)

                sg.popup("Timesheet Submitted", title="Success")
                break

        create_timesheet_window.close()
        return 
    
    def view_all_timesheets_page(self):
        timesheets = self.timesheet_handler.get_timesheets_by_status(self.user.department, "Pending")
        data = []

        if timesheets:
            for timesheet in timesheets:
                data.append([timesheet.timesheet_id, timesheet.employee_id, timesheet.department, timesheet.status])
        
        layout = [
            [sg.Text("Pending Timesheets")],
            [sg.Table(values=data, headings=["Timesheet ID", "Employee ID", "Department ID", "Status"], 
                      auto_size_columns=False, justification="right", num_rows=10, key="-TIMESHEET_TABLE-", enable_events=True)],
            [sg.Button("Exit")]
        ]
        
        view_all_timesheets_window = sg.Window("View All Timesheets", layout, icon=self.icon_path)

        while True:
            event, values = view_all_timesheets_window.read()

            if event == sg.WIN_CLOSED or event == "Exit":
                break

            if event == "-TIMESHEET_TABLE-":
                if len(values["-TIMESHEET_TABLE-"]) > 0:
                    selected_row = values["-TIMESHEET_TABLE-"][0]

                    self.approve_timesheet_page(timesheets[selected_row])

                    timesheets = self.timesheet_handler.get_timesheets_by_status(self.user.department, "Pending")
                    data = []

                    if timesheets:
                        for timesheet in timesheets:
                            data.append([timesheet.timesheet_id, timesheet.employee_id, timesheet.department_id, timesheet.status])
                        
                    view_all_timesheets_window["-TIMESHEET_TABLE-"].update(values=data)

        view_all_timesheets_window.close()
        return 

    def approve_timesheet_page(self, timesheet):
        layout = [
            [sg.Text("Timesheet Information")],
            [sg.Table(values=list(timesheet.worked_hours.items()), headings=["Date", "Hours"], 
                      auto_size_columns=False, justification="right", num_rows=10, key="-TIMESHEET_INFO-")],
            [sg.Button("Approve"), sg.Button("Deny"), sg.Button("Exit")]
        ]

        approve_timesheet_window = sg.Window("Approve Timesheet", layout, icon=self.icon_path)

        while True:
            event, values = approve_timesheet_window.read()

            if event == sg.WIN_CLOSED or event == "Exit":
                break

            elif event == "Approve":
                self.timesheet_handler.set_timesheet_status(timesheet.timesheet_id, "Approved")
                sg.popup("Timesheet Approved", title="Approved")
                break

            elif event == "Deny":
                self.timesheet_handler.set_timesheet_status(timesheet.timesheet_id, "Denied")
                sg.popup("Timesheet Denied", title="Denied")
                break

        approve_timesheet_window.close()
        return 

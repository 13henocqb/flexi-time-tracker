import PySimpleGUI

from model import DatabaseHandler
from presenter import UserHandler, TimesheetHandler
from view import FlexiTimeGUI

def main():
    # Model
    db_handler = DatabaseHandler("database.sqlite")
    # Presenter
    user_handler = UserHandler(db_handler)
    timesheet_handler = TimesheetHandler(db_handler)
    # View
    app = FlexiTimeGUI(user_handler, timesheet_handler, icon_path="icon.ico")

    # Start application
    app.main_page()

    # Closing connection to database is best practice
    db_handler.close()

if __name__ == "__main__":
    main()
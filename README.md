# Flexi-Time Application 

## Description
The Flexi-Time App is a simple Python application designed to help employees and managers manage flexible working hours and timesheets. This application uses the PySimpleGUI library to create a graphical user interface, making it user-friendly and easy to interact with.

## Features
The Flexi-Time App includes the following features:

1. **Log In**: 
    - Users can log in using their email and password. Depending on their role (Employee or Manager), they will have access to different functionalities.

2. **Employee Functionality**:
   - View and manage their Flexi Balance.
   - Create timesheets for tracking their working hours.

3. **Manager Functionality**:
   - View pending timesheets submitted by employees.
   - Approve or deny timesheets.

## Prerequisites
Before using the Flexi-Time App, make sure you have the following installed:
- Python 3
- PySimpleGUI library

## Installation
1. Clone this repository or download the source code.
2. Make sure you have Python and the required libraries installed. If you do not have PySimpleGUI, run the following command:
   ```
   pip install PySimpleGUI
   ```
3. Open the terminal and navigate to the directory where the app's source code is located.
4. Run the app by executing the following command:
   ```
   python main.py
   ```

## How to Use
1. Launch the application by running the `view.py` script.
2. Log in with a email and password.
    - For an employee, you can use "`john@example.com`" and "`password123`"
    - For a manager, you can use "`manager@example.com`" and "`qwerty`"
3. Depending on your role (Employee or Manager), you will have access to different functionalities.
4. Follow the on-screen instructions to create timesheets, view pending timesheets, and manage your Flexi Balance (if you are an employee).
5. Managers can approve or deny timesheets submitted by employees within their same department.

## Project Structure
The project structure is organised as follows:
- `view.py`: The main application script containing the user interface and application logic.
- `controller.py`: Controller classes for managing users and timesheets.
- `model.py`: Model structures for users and timesheets.
- `data_access.py`: Database handling and data access classes.
- `database.sqlite`: The SQLite database where user and timesheet data is stored.
- `icon.ico`: The application's icon.

## Acknowledgments
- PySimpleGUI: A simple Python GUI framework used for creating the user interface.

This application has been designed as a bare-bones shell upon which future expansion is encouraged.

Enjoy using the Flexi-Time App!

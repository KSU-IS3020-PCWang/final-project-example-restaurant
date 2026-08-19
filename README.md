# IS 3020 Final Project

## Student and Project Information

- Student name: Pengcheng Wang
- GitHub username: pcwangatl
- Project title: Restaurant Reservation System
- Application purpose: This application helps restaurant staff create and manage customer reservations through a graphical interface. It provides a consistent way to add, view, modify, delete, save, and review reservations.

## How to Run the Application

1. Open the project folder in PyCharm.
2. Confirm that `reservation_system.py` and the `data` folder are in the project root.
3. Confirm that Python 3 with Tkinter support is selected as the project interpreter.
4. Open `reservation_system.py`.
5. Click the green Run button or right-click the file and select **Run 'reservation_system'**.
6. Use the application window to manage reservations.

The program uses Python's built-in Tkinter library and does not require additional packages.

## Major Features

- Add a reservation with a customer name, phone number, date, time, and party size.
- Display saved reservations in a graphical table.
- Select a reservation to load its information into the entry fields.
- Modify or delete the selected reservation.
- Display a customer's reservation history using the phone number field.
- Refresh the table to display all reservations after viewing customer history.
- Prevent two reservations from using the same date and time.
- Display error and confirmation messages in dialog boxes.
- Save reservations automatically after successful changes and when the window closes.
- Load previously saved reservations when the application starts.

## Python Concepts Used

The application uses functions to load, save, find, validate, add, modify, and delete reservation records. A list stores the complete reservation collection, and dictionaries represent individual reservations. Conditionals validate information and control decisions, while loops and `for` loops process stored data. The program reads and writes a CSV file and uses `try/except` to handle missing files and invalid numeric input.

The final version also uses a lightweight `ReservationApp` class to organize Tkinter widgets and button-event functions. Tkinter variables connect the entry fields to Python values, and a `Treeview` widget displays reservations in a table. The original reservation functions remain separate from the graphical interface so their logic is easier to read and test.

## Data Files

The application stores its data in `data/reservations.csv`. The CSV file contains the following fields:

- `id`: a unique whole-number reservation ID
- `customer_name`: the customer's name
- `phone`: the customer's phone number, such as `404-123-1234`
- `date`: the reservation date in `YYYY-MM-DD` format
- `time`: the requested reservation time
- `party_size`: the number of guests

If the CSV file does not exist when the application starts, the program begins with an empty reservation list. The file is created when reservations are saved.

## Testing Summary

The reservation functions were tested by adding valid reservations, rejecting invalid information, preventing duplicate time slots, modifying and deleting records, searching customer history, saving a temporary CSV file, and loading the saved records again. The graphical interface was checked for the required entry fields, reservation table, button handlers, error messages, and guarded startup behavior. The final application should also be opened in PyCharm to confirm that the window displays correctly on the student's computer.

## AI Use

ChatGPT was used after the original command-line version was working. It helped design and add the graphical user interface while preserving the existing reservation and CSV functions. See `AI_USAGE.md` for the improvement record.

## GitHub Milestones

This project demonstrates the following required commits:

1. `Initial project setup`
2. `Original working version before AI improvement`
3. `Final version after AI improvement`

The final commit should include the GUI version of `reservation_system.py`, the completed `README.md`, and the completed `AI_USAGE.md`.

# IS 3020 Final Project

## Student and Project Information

- Student name: Pengcheng Wang
- GitHub username: pcwangatl
- Project title: Restaurant Reservation System
- Application purpose: This application helps restaurant staff create and manage customer reservations. It replaces scattered or handwritten reservation records with a consistent process for adding, viewing, modifying, deleting, saving, and reviewing reservations.

## How to Run the Application

1. Open the project folder in PyCharm.
2. Confirm that `reservation_system.py` and the `data` folder are in the project root.
3. Confirm that Python 3 is selected as the project interpreter.
4. Open `reservation_system.py`.
5. Click the green Run button or right-click the file and select **Run 'reservation_system'**.
6. Follow the numbered menu displayed in the Run window.

The program uses only the Python standard library. No additional packages are required.

## Major Features

- Add a reservation with a customer name, phone number, date, time, and party size.
- Display all saved reservations.
- Modify an existing reservation by its reservation ID.
- Delete an existing reservation by its reservation ID.
- Display a customer's reservation history by phone number.
- Prevent two reservations from using the same date and time.
- Save reservations automatically after a successful change and when the user exits.
- Load previously saved reservations when the program starts.

## Python Concepts Used

The application organizes its work into functions for loading, saving, finding, validating, adding, modifying, deleting, and displaying reservations. A list stores all reservation records, and each reservation is represented by a dictionary. Conditionals validate user choices and reservation information. A `while` loop keeps the menu running, and `for` loops search and display stored records. The program uses a CSV file for persistent storage and uses `try/except` to handle missing files and invalid whole-number input.

## Data Files

The application stores its data in `data/reservations.csv`. The CSV file contains the following fields:

- `id`: a unique whole-number reservation ID
- `customer_name`: the customer's name
- `phone`: the customer's phone number, such as `404-123-1234`
- `date`: the reservation date in `YYYY-MM-DD` format
- `time`: the requested reservation time
- `party_size`: the number of guests

If the CSV file does not exist when the program starts, the application begins with an empty reservation list. The file is created when reservations are saved.

## Testing Summary

The original command-line version was tested by adding valid reservations, rejecting missing or invalid information, preventing duplicate time slots, viewing all records, modifying and deleting records by ID, searching customer history by phone number, saving the CSV file, and restarting the program to confirm that saved reservations load correctly. Invalid menu choices and non-numeric ID or party-size entries were also tested.

## AI Use

AI was not used to add features to this original working version. This command-line application was preserved before the AI-assisted improvement stage. The next milestone will use ChatGPT to design and add a graphical user interface to the functional system.

## GitHub Milestone

After confirming that this version runs correctly, commit and push it with this message:

`Original working version before AI improvement`

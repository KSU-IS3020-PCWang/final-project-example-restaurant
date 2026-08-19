"""Restaurant reservation system with a Tkinter graphical interface.

The original application logic still uses functions, lists, dictionaries,
conditionals, loops, a CSV file, and try/except. ChatGPT was used to replace
the command-line menu with a simple graphical user interface.
"""

import tkinter as tk
from tkinter import messagebox, ttk


DATA_FILE = "data/reservations.csv"


# ------------------------------------------------------------
# File functions
# ------------------------------------------------------------

def load_reservations(file_name):
    """Read reservation records from a CSV file and return a list."""
    reservations = []

    try:
        with open(file_name, "r") as reservation_file:
            first_line = True

            for line in reservation_file:
                # The first row contains column names, not a reservation.
                if first_line:
                    first_line = False
                else:
                    parts = line.strip().split(",")

                    if len(parts) == 6:
                        try:
                            reservation = {
                                "id": int(parts[0]),
                                "customer_name": parts[1],
                                "phone": parts[2],
                                "date": parts[3],
                                "time": parts[4],
                                "party_size": int(parts[5]),
                            }
                            reservations.append(reservation)
                        except ValueError:
                            print("One invalid reservation row was skipped.")
    except FileNotFoundError:
        # A first-time user can begin without an existing data file.
        print("No reservation file was found. Starting with an empty list.")

    return reservations


def save_reservations(file_name, reservations):
    """Write all reservation records to a CSV file."""
    try:
        with open(file_name, "w") as reservation_file:
            reservation_file.write(
                "id,customer_name,phone,date,time,party_size\n"
            )

            for reservation in reservations:
                row = str(reservation["id"]) + ","
                row = row + reservation["customer_name"] + ","
                row = row + reservation["phone"] + ","
                row = row + reservation["date"] + ","
                row = row + reservation["time"] + ","
                row = row + str(reservation["party_size"]) + "\n"
                reservation_file.write(row)

        return True
    except FileNotFoundError:
        print("The reservation file could not be saved.")
        return False


# ------------------------------------------------------------
# Reservation functions
# ------------------------------------------------------------

def find_reservation(reservations, reservation_id):
    """Return the reservation with the requested ID, or return None."""
    for reservation in reservations:
        if reservation["id"] == reservation_id:
            return reservation

    return None


def is_time_slot_available(
    reservations, date, time, ignored_reservation_id
):
    """Check whether a date and time are available."""
    for reservation in reservations:
        same_date = reservation["date"] == date
        same_time = reservation["time"] == time
        different_reservation = reservation["id"] != ignored_reservation_id

        if same_date and same_time and different_reservation:
            return False

    return True


def add_reservation(
    reservations, customer_name, phone, date, time, party_size
):
    """Validate and add one reservation. Return the new record or None."""
    missing_information = (
        customer_name == "" or phone == "" or date == "" or time == ""
    )
    invalid_csv_text = "," in customer_name or "," in phone

    if missing_information or invalid_csv_text or party_size <= 0:
        return None

    if not is_time_slot_available(reservations, date, time, 0):
        return None

    # Select an ID that is higher than every existing reservation ID.
    next_id = 1
    for reservation in reservations:
        if reservation["id"] >= next_id:
            next_id = reservation["id"] + 1

    new_reservation = {
        "id": next_id,
        "customer_name": customer_name,
        "phone": phone,
        "date": date,
        "time": time,
        "party_size": party_size,
    }
    reservations.append(new_reservation)
    return new_reservation


def modify_reservation(
    reservations,
    reservation_id,
    customer_name,
    phone,
    date,
    time,
    party_size,
):
    """Replace the information in an existing reservation."""
    reservation = find_reservation(reservations, reservation_id)

    if reservation is None:
        return False

    missing_information = (
        customer_name == "" or phone == "" or date == "" or time == ""
    )
    invalid_csv_text = "," in customer_name or "," in phone

    if missing_information or invalid_csv_text or party_size <= 0:
        return False

    if not is_time_slot_available(
        reservations, date, time, reservation_id
    ):
        return False

    reservation["customer_name"] = customer_name
    reservation["phone"] = phone
    reservation["date"] = date
    reservation["time"] = time
    reservation["party_size"] = party_size
    return True


def delete_reservation(reservations, reservation_id):
    """Remove the requested reservation and report whether it was found."""
    reservation = find_reservation(reservations, reservation_id)

    if reservation is None:
        return False

    reservations.remove(reservation)
    return True


def get_customer_history(reservations, phone):
    """Return all reservations that match one customer's phone number."""
    customer_history = []

    for reservation in reservations:
        if reservation["phone"] == phone:
            customer_history.append(reservation)

    return customer_history


# ------------------------------------------------------------
# Graphical user interface
# ------------------------------------------------------------

class ReservationApp:
    """Create and control the restaurant reservation window."""

    def __init__(self, root, data_file=DATA_FILE):
        """Load data, create GUI variables, and build the window."""
        self.root = root
        self.data_file = data_file
        self.reservations = load_reservations(data_file)
        self.selected_reservation_id = None

        self.customer_name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.time_var = tk.StringVar()
        self.party_size_var = tk.StringVar()

        self.root.title("Restaurant Reservation System")
        self.root.geometry("920x560")
        self.root.minsize(820, 500)

        self.build_form()
        self.build_buttons()
        self.build_table()
        self.refresh_tree()

        # Use the same save-and-close process for the window close button.
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    def build_form(self):
        """Create the labeled reservation entry fields."""
        form_frame = ttk.LabelFrame(
            self.root, text="Reservation Information", padding=12
        )
        form_frame.pack(fill="x", padx=12, pady=(12, 6))

        fields = [
            ("Customer name", self.customer_name_var),
            ("Phone (404-123-1234)", self.phone_var),
            ("Date (YYYY-MM-DD)", self.date_var),
            ("Time (6:00 PM)", self.time_var),
            ("Party size", self.party_size_var),
        ]

        for column, field in enumerate(fields):
            label_text, variable = field
            ttk.Label(form_frame, text=label_text).grid(
                row=0, column=column, padx=5, pady=3, sticky="w"
            )
            ttk.Entry(form_frame, textvariable=variable, width=18).grid(
                row=1, column=column, padx=5, pady=3, sticky="ew"
            )
            form_frame.columnconfigure(column, weight=1)

    def build_buttons(self):
        """Create buttons and connect each button to its event handler."""
        button_frame = ttk.Frame(self.root, padding=(12, 6))
        button_frame.pack(fill="x")

        buttons = [
            ("Add", self.add_from_form),
            ("Modify Selected", self.modify_selected),
            ("Delete Selected", self.delete_selected),
            ("Customer History", self.show_customer_history),
            ("Refresh All", self.refresh_tree),
            ("Exit", self.close_app),
        ]

        for button_text, command in buttons:
            ttk.Button(
                button_frame, text=button_text, command=command
            ).pack(side="left", padx=4)

    def build_table(self):
        """Create the table that displays reservation records."""
        table_frame = ttk.Frame(self.root, padding=(12, 6, 12, 12))
        table_frame.pack(fill="both", expand=True)

        columns = (
            "id",
            "customer_name",
            "phone",
            "date",
            "time",
            "party_size",
        )
        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", height=15
        )

        headings = {
            "id": "ID",
            "customer_name": "Customer",
            "phone": "Phone",
            "date": "Date",
            "time": "Time",
            "party_size": "Party Size",
        }
        widths = {
            "id": 55,
            "customer_name": 180,
            "phone": 130,
            "date": 110,
            "time": 100,
            "party_size": 85,
        }

        for column in columns:
            self.tree.heading(column, text=headings[column])
            self.tree.column(column, width=widths[column], anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Selecting a row loads that reservation into the entry fields.
        self.tree.bind("<<TreeviewSelect>>", self.load_selected_reservation)

    def get_form_values(self):
        """Return stripped form values and convert party size to an integer."""
        customer_name = self.customer_name_var.get().strip()
        phone = self.phone_var.get().strip()
        date = self.date_var.get().strip()
        time = self.time_var.get().strip()
        party_size = int(self.party_size_var.get().strip())
        return customer_name, phone, date, time, party_size

    def refresh_tree(self, reservations_to_show=None):
        """Replace the table contents with all or selected reservations."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        records = self.reservations
        if reservations_to_show is not None:
            records = reservations_to_show

        for reservation in records:
            self.tree.insert(
                "",
                "end",
                values=(
                    reservation["id"],
                    reservation["customer_name"],
                    reservation["phone"],
                    reservation["date"],
                    reservation["time"],
                    reservation["party_size"],
                ),
            )

    def load_selected_reservation(self, event=None):
        """Copy the selected table row into the entry fields."""
        selected_items = self.tree.selection()
        if len(selected_items) == 0:
            return

        values = self.tree.item(selected_items[0], "values")
        self.selected_reservation_id = int(values[0])
        self.customer_name_var.set(values[1])
        self.phone_var.set(values[2])
        self.date_var.set(values[3])
        self.time_var.set(values[4])
        self.party_size_var.set(values[5])

    def clear_form(self):
        """Clear the form and remove the current table selection."""
        self.customer_name_var.set("")
        self.phone_var.set("")
        self.date_var.set("")
        self.time_var.set("")
        self.party_size_var.set("")
        self.selected_reservation_id = None

        for selected_item in self.tree.selection():
            self.tree.selection_remove(selected_item)

    def save_changes(self):
        """Save current records and display an error if saving fails."""
        if save_reservations(self.data_file, self.reservations):
            return True

        messagebox.showerror(
            "Save Error",
            "The reservation data could not be saved. Check the data folder.",
        )
        return False

    def add_from_form(self):
        """Add a reservation using the current form values."""
        try:
            form_values = self.get_form_values()
        except ValueError:
            messagebox.showerror(
                "Invalid Party Size", "Party size must be a whole number."
            )
            return

        new_reservation = add_reservation(
            self.reservations, *form_values
        )
        if new_reservation is None:
            messagebox.showerror(
                "Reservation Not Added",
                "Complete every field, use a positive party size, and choose "
                "an available time slot.",
            )
            return

        if self.save_changes():
            self.refresh_tree()
            self.clear_form()
            messagebox.showinfo(
                "Reservation Added",
                f'Reservation {new_reservation["id"]} was added.',
            )

    def modify_selected(self):
        """Replace the selected reservation with the current form values."""
        if self.selected_reservation_id is None:
            messagebox.showerror(
                "No Selection", "Select a reservation before modifying it."
            )
            return

        try:
            form_values = self.get_form_values()
        except ValueError:
            messagebox.showerror(
                "Invalid Party Size", "Party size must be a whole number."
            )
            return

        was_modified = modify_reservation(
            self.reservations,
            self.selected_reservation_id,
            *form_values,
        )
        if not was_modified:
            messagebox.showerror(
                "Reservation Not Modified",
                "Check the information and confirm that the time is available.",
            )
            return

        if self.save_changes():
            self.refresh_tree()
            self.clear_form()
            messagebox.showinfo(
                "Reservation Modified", "The reservation was modified."
            )

    def delete_selected(self):
        """Delete the selected reservation after user confirmation."""
        if self.selected_reservation_id is None:
            messagebox.showerror(
                "No Selection", "Select a reservation before deleting it."
            )
            return

        confirmed = messagebox.askyesno(
            "Delete Reservation",
            "Are you sure you want to delete the selected reservation?",
        )
        if not confirmed:
            return

        if delete_reservation(
            self.reservations, self.selected_reservation_id
        ):
            if self.save_changes():
                self.refresh_tree()
                self.clear_form()
                messagebox.showinfo(
                    "Reservation Deleted", "The reservation was deleted."
                )

    def show_customer_history(self):
        """Display reservations matching the phone number in the form."""
        phone = self.phone_var.get().strip()
        if phone == "":
            messagebox.showerror(
                "Phone Required",
                "Enter a phone number before viewing customer history.",
            )
            return

        customer_history = get_customer_history(self.reservations, phone)
        self.refresh_tree(customer_history)

        if len(customer_history) == 0:
            messagebox.showinfo(
                "No Customer History",
                "No reservations were found for that phone number.",
            )

    def close_app(self):
        """Save current records and close the graphical application."""
        if self.save_changes():
            self.root.destroy()


def main():
    """Create the Tkinter window and start its event loop."""
    root = tk.Tk()
    ReservationApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

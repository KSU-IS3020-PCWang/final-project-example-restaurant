"""Restaurant reservation system example for IS 3020.

This program demonstrates how the concepts from the course can work together
in one small application. It uses a menu, functions, lists, dictionaries,
conditionals, loops, a CSV file, and try/except.
"""


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
        # An empty list lets a first-time user begin with no saved records.
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

    # Find an ID that is higher than every existing reservation ID.
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
# Display and menu functions
# ------------------------------------------------------------

def display_reservations(reservations):
    """Print reservation records in a readable format."""
    if len(reservations) == 0:
        print("No reservations were found.")
    else:
        for reservation in reservations:
            print("-" * 40)
            print(f'ID: {reservation["id"]}')
            print(f'Customer: {reservation["customer_name"]}')
            print(f'Phone: {reservation["phone"]}')
            print(f'Date: {reservation["date"]}')
            print(f'Time: {reservation["time"]}')
            print(f'Party size: {reservation["party_size"]}')


def main():
    """Run the menu until the user chooses to exit."""
    reservations = load_reservations(DATA_FILE)
    running = True

    while running:
        print("\nRESTAURANT RESERVATION SYSTEM")
        print("1. Add a reservation")
        print("2. View all reservations")
        print("3. Modify a reservation")
        print("4. Delete a reservation")
        print("5. View customer history")
        print("6. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            customer_name = input("Customer name: ").strip()
            phone = input("Phone number: ").strip()
            date = input("Date (YYYY-MM-DD): ").strip()
            time = input("Time (example: 6:00 PM): ").strip()

            try:
                party_size = int(input("Party size: "))
                new_reservation = add_reservation(
                    reservations,
                    customer_name,
                    phone,
                    date,
                    time,
                    party_size,
                )

                if new_reservation is None:
                    print("The reservation could not be added.")
                    print("Check the information and time slot.")
                else:
                    save_reservations(DATA_FILE, reservations)
                    print(f'Reservation {new_reservation["id"]} was added.')
            except ValueError:
                print("Party size must be a whole number.")

        elif choice == "2":
            display_reservations(reservations)

        elif choice == "3":
            display_reservations(reservations)

            try:
                reservation_id = int(input("Reservation ID to modify: "))
                customer_name = input("New customer name: ").strip()
                phone = input("New phone number: ").strip()
                date = input("New date (YYYY-MM-DD): ").strip()
                time = input("New time (example: 6:00 PM): ").strip()
                party_size = int(input("New party size: "))

                was_modified = modify_reservation(
                    reservations,
                    reservation_id,
                    customer_name,
                    phone,
                    date,
                    time,
                    party_size,
                )

                if was_modified:
                    save_reservations(DATA_FILE, reservations)
                    print("The reservation was modified.")
                else:
                    print("The reservation could not be modified.")
            except ValueError:
                print("The ID and party size must be whole numbers.")

        elif choice == "4":
            display_reservations(reservations)

            try:
                reservation_id = int(input("Reservation ID to delete: "))

                if delete_reservation(reservations, reservation_id):
                    save_reservations(DATA_FILE, reservations)
                    print("The reservation was deleted.")
                else:
                    print("That reservation ID was not found.")
            except ValueError:
                print("The reservation ID must be a whole number.")

        elif choice == "5":
            phone = input("Customer phone number: ").strip()
            customer_history = get_customer_history(reservations, phone)
            display_reservations(customer_history)

        elif choice == "6":
            save_reservations(DATA_FILE, reservations)
            running = False
            print("Reservations saved. Goodbye.")

        else:
            print("Please choose a number from 1 through 6.")


if __name__ == "__main__":
    main()

# ==================================================
# MATATU FARE COLLECTION SYSTEM
# VERSION 2.0
# ==================================================

import sqlite3
from datetime import datetime


# ==================================================
# DATABASE CONNECTION
# ==================================================

connection = sqlite3.connect("matatu.db")
cursor = connection.cursor()


# ==================================================
# CREATE DATABASE TABLE
# ==================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS collections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle TEXT NOT NULL,
    driver TEXT NOT NULL DEFAULT 'Not recorded',
    date TEXT NOT NULL,
    passengers INTEGER NOT NULL,
    total REAL NOT NULL
)
""")

# Upgrade an existing database without deleting records.
# Add the driver column only if it does not already exist.

cursor.execute("PRAGMA table_info(collections)")
columns = [column[1] for column in cursor.fetchall()]

if "driver" not in columns:
    cursor.execute("""
    ALTER TABLE collections
    ADD COLUMN driver TEXT NOT NULL DEFAULT 'Not recorded'
    """)

connection.commit()


# ==================================================
# FUNCTION 1: RECORD A COLLECTION
# ==================================================

def record_collection():

    print("\n========================================")
    print("             RECORD COLLECTION")
    print("========================================")

    vehicle = input("Enter vehicle registration: ").strip().upper()

    if not vehicle:
        print("Vehicle registration cannot be empty.")
        return

    driver = input("Enter driver's name: ").strip()

    if not driver:
        print("Driver's name cannot be empty.")
        return

    try:
        passengers = int(input("Enter number of passengers: "))

        if passengers <= 0:
            print("Passengers must be greater than zero.")
            return

        fares = []

        for number in range(1, passengers + 1):

            fare = float(
                input(
                    f"Enter fare for passenger {number} (KSh): "
                )
            )

            if fare <= 0:
                print("Fare must be greater than zero.")
                return

            fares.append(fare)

        total = sum(fares)

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
        INSERT INTO collections
        (vehicle, driver, date, passengers, total)
        VALUES (?, ?, ?, ?, ?)
        """, (vehicle, driver, date, passengers, total))

        connection.commit()

        print("\nCollection saved successfully!")
        print("----------------------------------------")
        print("Vehicle:", vehicle)
        print("Driver:", driver)
        print("Date:", date)
        print("Passengers:", passengers)
        print(f"Total collected: KSh {total:.2f}")
        print("----------------------------------------")

    except ValueError:
        print("Invalid input. Enter valid numbers.")


# ==================================================
# FUNCTION 2: VIEW ALL COLLECTIONS
# ==================================================

def view_collections():

    print("\n========================================")
    print("           COLLECTION HISTORY")
    print("========================================")

    cursor.execute("""
    SELECT id, vehicle, driver, date, passengers, total
    FROM collections
    ORDER BY id DESC
    """)

    records = cursor.fetchall()

    if not records:
        print("No collection records found.")
        return

    for record in records:

        print("\n----------------------------------------")
        print("Record ID:", record[0])
        print("Vehicle:", record[1])
        print("Driver:", record[2])
        print("Date:", record[3])
        print("Passengers:", record[4])
        print(f"Total: KSh {record[5]:.2f}")

    print("----------------------------------------")


# ==================================================
# FUNCTION 3: DAILY COLLECTION REPORT
# ==================================================

def daily_report():

    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
    SELECT
        vehicle,
        COUNT(*),
        SUM(passengers),
        SUM(total)
    FROM collections
    WHERE date(date) = ?
    GROUP BY vehicle
    ORDER BY vehicle
    """, (today,))

    records = cursor.fetchall()

    print("\n========================================")
    print("        DAILY COLLECTION REPORT")
    print("========================================")
    print("Date:", today)

    if not records:
        print("No collections recorded today.")
        return

    fleet_total = 0
    fleet_passengers = 0
    fleet_collections = 0

    for record in records:

        vehicle = record[0]
        collections = record[1]
        passengers = record[2]
        total = record[3]

        print("\nVehicle:", vehicle)
        print("Number of collections:", collections)
        print("Total passengers:", passengers)
        print(f"Total collected: KSh {total:.2f}")

        fleet_total += total
        fleet_passengers += passengers
        fleet_collections += collections

    print("\n========================================")
    print("           FLEET SUMMARY")
    print("========================================")
    print("Total collections:", fleet_collections)
    print("Total passengers:", fleet_passengers)
    print(f"TOTAL COLLECTED: KSh {fleet_total:.2f}")
    print("========================================")


# ==================================================
# MAIN MENU
# ==================================================

try:

    while True:

        print("\n========================================")
        print("       MATATU FARE COLLECTION SYSTEM")
        print("                 VERSION 2.0")
        print("========================================")

        print("1. Record a Collection")
        print("2. View All Collections")
        print("3. Daily Collection Report")
        print("4. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            record_collection()

        elif choice == "2":
            view_collections()

        elif choice == "3":
            daily_report()

        elif choice == "4":
            print("Thank you for using the system!")
            break

        else:
            print("Invalid choice. Select 1, 2, 3, or 4.")

finally:

    connection.close()

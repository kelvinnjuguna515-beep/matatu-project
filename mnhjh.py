# ==================================================
# MATATU FARE COLLECTION SYSTEM
# VERSION 3.0
# ==================================================

import sqlite3
from datetime import datetime


# DATABASE CONNECTION
connection = sqlite3.connect("matatu.db")
cursor = connection.cursor()


# CREATE TABLE AND UPGRADE OLD DATABASE
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

cursor.execute("PRAGMA table_info(collections)")
columns = [column[1] for column in cursor.fetchall()]

if "driver" not in columns:
    cursor.execute("""
    ALTER TABLE collections
    ADD COLUMN driver TEXT NOT NULL DEFAULT 'Not recorded'
    """)

connection.commit()


# 1. RECORD COLLECTION
def record_collection():

    print("\n===== RECORD COLLECTION =====")

    vehicle = input("Vehicle registration: ").strip().upper()
    driver = input("Driver's name: ").strip()

    if not vehicle or not driver:
        print("Vehicle and driver's name are required.")
        return

    try:
        passengers = int(input("Number of passengers: "))

        if passengers <= 0:
            print("Passengers must be greater than zero.")
            return

        total = 0

        for number in range(1, passengers + 1):
            fare = float(
                input(f"Fare for passenger {number} (KSh): ")
            )

            if fare <= 0:
                print("Fare must be greater than zero.")
                return

            total += fare

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
        INSERT INTO collections
        (vehicle, driver, date, passengers, total)
        VALUES (?, ?, ?, ?, ?)
        """, (vehicle, driver, date, passengers, total))

        connection.commit()

        print("\nCollection saved successfully!")
        print("Vehicle:", vehicle)
        print("Driver:", driver)
        print("Passengers:", passengers)
        print(f"Total collected: KSh {total:.2f}")

    except ValueError:
        print("Invalid number. Please enter valid numbers.")


# 2. VIEW ALL COLLECTIONS
def view_collections():

    print("\n===== COLLECTION HISTORY =====")

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
        print("\n--------------------------------")
        print("Record ID:", record[0])
        print("Vehicle:", record[1])
        print("Driver:", record[2])
        print("Date:", record[3])
        print("Passengers:", record[4])
        print(f"Total: KSh {record[5]:.2f}")


# 3. DAILY COLLECTION REPORT
def daily_report():

    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
    SELECT vehicle, COUNT(*), SUM(passengers), SUM(total)
    FROM collections
    WHERE date(date) = ?
    GROUP BY vehicle
    ORDER BY vehicle
    """, (today,))

    records = cursor.fetchall()

    print("\n===== DAILY COLLECTION REPORT =====")
    print("Date:", today)

    if not records:
        print("No collections recorded today.")
        return

    fleet_total = 0
    fleet_passengers = 0
    fleet_collections = 0

    for record in records:
        print("\nVehicle:", record[0])
        print("Collections:", record[1])
        print("Passengers:", record[2])
        print(f"Total: KSh {record[3]:.2f}")

        fleet_collections += record[1]
        fleet_passengers += record[2]
        fleet_total += record[3]

    print("\n===== FLEET SUMMARY =====")
    print("Collections:", fleet_collections)
    print("Passengers:", fleet_passengers)
    print(f"Total collected: KSh {fleet_total:.2f}")


# 4. SEARCH VEHICLE
def search_vehicle():

    print("\n===== SEARCH VEHICLE =====")

    vehicle = input(
        "Enter vehicle registration: "
    ).strip().upper()

    if not vehicle:
        print("Vehicle registration is required.")
        return

    cursor.execute("""
    SELECT id, vehicle, driver, date, passengers, total
    FROM collections
    WHERE UPPER(vehicle) = ?
    ORDER BY id DESC
    """, (vehicle,))

    records = cursor.fetchall()

    if not records:
        print("No records found for", vehicle)
        return

    total_collected = 0
    total_passengers = 0

    for record in records:
        print("\n--------------------------------")
        print("Record ID:", record[0])
        print("Vehicle:", record[1])
        print("Driver:", record[2])
        print("Date:", record[3])
        print("Passengers:", record[4])
        print(f"Collection: KSh {record[5]:.2f}")

        total_passengers += record[4]
        total_collected += record[5]

    print("\n===== VEHICLE SUMMARY =====")
    print("Vehicle:", vehicle)
    print("Number of collections:", len(records))
    print("Total passengers:", total_passengers)
    print(f"Total collected: KSh {total_collected:.2f}")


# 5. MAIN MENU
try:
    while True:

        print("\n===================================")
        print(" MATATU FARE COLLECTION SYSTEM")
        print(" VERSION 3.0")
        print("===================================")
        print("1. Record a Collection")
        print("2. View All Collections")
        print("3. Daily Collection Report")
        print("4. Search Vehicle")
        print("5. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            record_collection()

        elif choice == "2":
            view_collections()

        elif choice == "3":
            daily_report()

        elif choice == "4":
            search_vehicle()

        elif choice == "5":
            print("Thank you for using the system!")
            break

        else:
            print("Invalid choice. Select 1, 2, 3, 4, or 5.")

finally:
    connection.close()

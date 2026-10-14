# ==================================================
# MATATU FARE COLLECTION SYSTEM
# Version 1.0
# ==================================================

import sqlite3
from datetime import datetime


# ==================================================
# DATABASE SETUP
# ==================================================

connection = sqlite3.connect("matatu.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS collections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle TEXT NOT NULL,
    date TEXT NOT NULL,
    passengers INTEGER NOT NULL,
    total REAL NOT NULL
)
""")

connection.commit()


# ==================================================
# FUNCTION 1: RECORD A COLLECTION
# ==================================================

def record_collection():

    print("\n===== RECORD COLLECTION =====")

    vehicle = input("Enter vehicle registration: ").strip().upper()

    if not vehicle:
        print("Vehicle registration cannot be empty.")
        return

    try:
        passengers = int(input("Enter number of passengers: "))

        if passengers <= 0:
            print("Number of passengers must be greater than zero.")
            return

        fares = []

        for number in range(1, passengers + 1):

            fare = float(
                input(f"Enter fare for passenger {number} (KSh): ")
            )

            if fare <= 0:
                print("Fare must be greater than zero.")
                return

            fares.append(fare)

        total = sum(fares)

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
        INSERT INTO collections (vehicle, date, passengers, total)
        VALUES (?, ?, ?, ?)
        """, (vehicle, date, passengers, total))

        connection.commit()

        print("\nCollection saved successfully!")
        print("Vehicle:", vehicle)
        print("Date:", date)
        print("Passengers:", passengers)
        print(f"Total collected: KSh {total:.2f}")

    except ValueError:
        print("Invalid input. Please enter numbers correctly.")


# ==================================================
# FUNCTION 2: VIEW ALL COLLECTIONS
# ==================================================

def view_collections():

    print("\n===== COLLECTION HISTORY =====")

    cursor.execute("""
    SELECT id, vehicle, date, passengers, total
    FROM collections
    ORDER BY id DESC
    """)

    records = cursor.fetchall()

    if not records:
        print("No collection records found.")
        return

    for record in records:

        print("-" * 40)
        print("Record ID:", record[0])
        print("Vehicle:", record[1])
        print("Date:", record[2])
        print("Passengers:", record[3])
        print(f"Total: KSh {record[4]:.2f}")


# ==================================================
# FUNCTION 3: DAILY COLLECTION REPORT
# ==================================================

def daily_report():

    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
    SELECT
        vehicle,
        COUNT(*) AS collections,
        SUM(passengers) AS total_passengers,
        SUM(total) AS total_collected
    FROM collections
    WHERE date(date) = ?
    GROUP BY vehicle
    ORDER BY vehicle
    """, (today,))

    records = cursor.fetchall()

    print("\n========================================")
    print("          DAILY COLLECTION REPORT")
    print("========================================")
    print("Date:", today)

    if not records:
        print("No collections recorded today.")
        return

    fleet_total = 0

    for record in records:

        vehicle = record[0]
        collections = record[1]
        passengers = record[2]
        total = record[3]

        print("\nVehicle:", vehicle)
        print("Collections:", collections)
        print("Total passengers:", passengers)
        print(f"Total collected: KSh {total:.2f}")

        fleet_total += total

    print("\n========================================")
    print(f"TOTAL FLEET COLLECTION: KSh {fleet_total:.2f}")
    print("========================================")


# ==================================================
# MAIN MENU
# ==================================================

try:

    while True:

        print("\n========================================")
        print("     MATATU FARE COLLECTION SYSTEM")
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

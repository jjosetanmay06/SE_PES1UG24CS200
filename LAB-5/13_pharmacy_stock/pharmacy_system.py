
"""Pharmacy stock management and prescription handling."""

import json
import sqlite3
from datetime import datetime

# Application state
conn = sqlite3.connect(":memory:")
stock = {}
prescriptions = []


def setup_database():
    """Create the patients table and insert sample patients."""
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE patients (id TEXT, name TEXT, allergy TEXT)"
    )
    cur.execute("INSERT INTO patients VALUES (?, ?, ?)",
                ("P1", "Kavya", "penicillin"))
    cur.execute("INSERT INTO patients VALUES (?, ?, ?)",
                ("P2", "Arjun", "none"))
    cur.execute("INSERT INTO patients VALUES (?, ?, ?)",
                ("P3", "Meena", "ibuprofen"))
    conn.commit()


def find_patient(name):
    """Find a patient by name using a parameterized query."""
    cur = conn.cursor()
    query = "SELECT id, allergy FROM patients WHERE name = ?"
    return cur.execute(query, (name,)).fetchall()


def add_stock(drug, units, expiry, batch_log=None):
    """Add stock and record the batch in an optional log."""
    if batch_log is None:
        batch_log = []

    stock[drug] = {
        "units": stock.get(drug, {}).get("units", 0) + units,
        "expiry": expiry,
    }
    batch_log.append((drug, units))
    return len(batch_log)


def dispense(patient_name, drug, units):
    """Dispense medication if the patient and stock are valid."""
    patients = find_patient(patient_name)
    if not patients:
        return False

    patient = patients[0]
    if patient[1].lower() != "none" and (
        patient[1].lower() == drug.lower()
    ):
        print("Allergy warning for", patient_name)
        return False

    if drug not in stock or stock[drug]["units"] < units:
        return False

    if units <= 0:
        return False

    stock[drug]["units"] -= units
    prescriptions.append({
        "patient": patient[0],
        "drug": drug,
        "units": units,
        "time": str(datetime.now()),
    })
    return True


def expiring_soon(days=30):
    """Return drugs expiring within the specified number of days."""
    soon = []
    now = datetime.now()

    for drug, details in stock.items():
        expiry = datetime.strptime(details["expiry"], "%Y-%m-%d")
        if (expiry - now).days < days:
            soon.append(drug)

    return soon


def export_prescriptions(file="prescriptions.json"):
    """Export prescriptions to a JSON file."""
    with open(file, "w", encoding="utf-8") as output_file:
        json.dump(prescriptions, output_file, indent=2)


def load_stock(file="stock.json"):
    """Load stock from JSON, returning an empty dictionary if unavailable."""
    try:
        with open(file, "r", encoding="utf-8") as input_file:
            loaded_stock = json.load(input_file)
    except FileNotFoundError:
        return {}
    except (json.JSONDecodeError, OSError) as error:
        print(f"Could not load stock: {error}")
        return {}

    if not isinstance(loaded_stock, dict):
        print("Could not load stock: expected a JSON object.")
        return {}

    return loaded_stock


def print_stock():
    """Print all current pharmacy stock."""
    print("Pharmacy Stock")
    for drug, details in stock.items():
        print(
            f"{drug} -> {details['units']} units, "
            f"expires {details['expiry']}"
        )


def main():
    """Run the pharmacy demonstration."""
    setup_database()
    stock.update(load_stock())

    add_stock("Paracetamol", 100, "2027-03-01")
    add_stock("Amoxicillin", 20, "2025-12-31")
    add_stock("Penicillin", 50, "2027-01-15")
    add_stock("Ibuprofen", 15, "2026-11-30")

    print("Arjun gets Amoxicillin:",
          dispense("Arjun", "Amoxicillin", 30))
    print("Kavya gets Penicillin:",
          dispense("Kavya", "Penicillin", 10))
    print("Meena gets ibuprofen:",
          dispense("Meena", "ibuprofen", 2))
    print("Unknown patient:", dispense("Ghost", "Paracetamol", 5))

    name = input("Patient name to look up (Enter for Arjun): ") or "Arjun"
    print("Lookup result:", find_patient(name))
    print("Expiring within 30 days:", expiring_soon())
    export_prescriptions()
    print_stock()


if __name__ == "__main__":
    main()

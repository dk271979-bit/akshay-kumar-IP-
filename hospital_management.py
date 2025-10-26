import mysql.connector

# --- Database configuration ---
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Popatlal@25"
DB_NAME = "hospital_management"

def create_connection():
    """Establishes and returns a database connection."""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def add_patient():
    """Adds a new patient to the database."""
    conn = create_connection()
    if conn is None:
        return

    name = input("Enter patient's name: ")
    try:
        age = int(input("Enter patient's age: "))
    except ValueError:
        print("Invalid age. Please enter a number.")
        conn.close()
        return

    diagnosis = input("Enter patient's diagnosis: ")

    cursor = conn.cursor()
    query = "INSERT INTO patients (name, age, diagnosis) VALUES (%s, %s, %s)"
    try:
        cursor.execute(query, (name, age, diagnosis))
        conn.commit()
        print("Patient added successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def view_all_patients():
    """Displays all patient records."""
    conn = create_connection()
    if conn is None:
        return

    cursor = conn.cursor()
    query = "SELECT * FROM patients"
    try:
        cursor.execute(query)
        patients = cursor.fetchall()

        if not patients:
            print("No patient records found.")
        else:
            print("\n--- All Patients ---")
            for patient in patients:
                print(f"ID: {patient[0]}, Name: {patient[1]}, Age: {patient[2]}, Diagnosis: {patient[3]}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def search_patient():
    """Searches for a patient by ID."""
    conn = create_connection()
    if conn is None:
        return
        
    try:
        patient_id = int(input("Enter patient ID to search: "))
    except ValueError:
        print("Invalid ID. Please enter a number.")
        conn.close()
        return
        
    cursor = conn.cursor()
    query = "SELECT * FROM patients WHERE patient_id = %s"
    try:
        cursor.execute(query, (patient_id,))
        patient = cursor.fetchone()
        
        if patient:
            print("\n--- Patient Found ---")
            print(f"ID: {patient[0]}, Name: {patient[1]}, Age: {patient[2]}, Diagnosis: {patient[3]}")
        else:
            print(f"Patient with ID {patient_id} not found.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def delete_patient():
    """Deletes a patient record by ID."""
    conn = create_connection()
    if conn is None:
        return
        
    try:
        patient_id = int(input("Enter patient ID to delete: "))
    except ValueError:
        print("Invalid ID. Please enter a number.")
        conn.close()
        return

    cursor = conn.cursor()
    query = "DELETE FROM patients WHERE patient_id = %s"
    try:
        cursor.execute(query, (patient_id,))
        conn.commit()
        
        if cursor.rowcount > 0:
            print(f"Patient with ID {patient_id} deleted successfully.")
        else:
            print(f"Patient with ID {patient_id} not found.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def main_menu():
    """Displays the main menu and handles user input."""
    while True:
        print("\n--- Hospital Management System ---")
        print("1. Add a new patient")
        print("2. View all patients")
        print("3. Search for a patient")
        print("4. Delete a patient record")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_patient()
        elif choice == '2':
            view_all_patients()
        elif choice == '3':
            search_patient()
        elif choice == '4':
            delete_patient()
        elif choice == '5':
            print("Exiting application.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()

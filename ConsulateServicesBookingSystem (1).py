import mysql.connector
from mysql.connector import Error
import unittest

class Appointment:
    def __init__(self, name, service, date, time):
        self.name = name
        self.service = service
        self.date = date
        self.time = time

    def __str__(self):
        return f"Appointment for {self.name}: {self.service} on {self.date} at {self.time}"

class ConsulateBookingSystem:
    def __init__(self):
        self.appointments = {}

    def book_appointment(self, name, service, date, time):
        appointment_id = len(self.appointments) + 1
        appointment = Appointment(name, service, date, time)
        self.appointments[appointment_id] = appointment
        print(f"Appointment booked successfully! ID: {appointment_id}")

    def cancel_appointment(self, appointment_id):
        if appointment_id in self.appointments:
            del self.appointments[appointment_id]
            print("Appointment canceled successfully!")
        else:
            print("Invalid appointment ID!")

    def view_appointments(self):
        if not self.appointments:
            print("No appointments scheduled.")
            return
        for appointment_id, appointment in self.appointments.items():
            print(f"ID: {appointment_id}, {appointment}")

class AppointmentAdmin:
    def __init__(self, host, user, password, database):
        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            if self.conn.is_connected():
                print("Connected to MySQL Database")
                self.cursor = self.conn.cursor()
            else:
                print("Connection to MySQL failed.")
                self.cursor = None
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.conn = None
            self.cursor = None

    def add_appointment_holder(self, appointment):
        if self.cursor is None:
            print("Cannot add Appointment Holder Details. No database connection.")
            return
        try:
            query = "INSERT INTO service (name, service, date, time) VALUES (%s, %s, %s, %s)"
            values = (appointment.name, appointment.service, appointment.date, appointment.time)
            self.cursor.execute(query, values)
            self.conn.commit()
            print(f"Account record for {appointment.name} added.")
        except Error as e:
            print(f"Failed to insert record: {e}")

    def details(self):
        if self.cursor is None:
            print("Cannot fetch Appointment Holder Details. No database connection.")
            return
        try:
            query = "SELECT * FROM service"
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            print('----**Details**---')
            for row in results:
                print(row)
        except Error as e:
            print(f'Failed to fetch details: {e}')

def main():
    system = ConsulateBookingSystem()
    admin = AppointmentAdmin("localhost", "root", "user", "passport_renewal")

    while True:
        print("\nConsulate Services Booking System")
        print("1. Book Appointment")
        print("2. Cancel Appointment")
        print("3. View Appointments")
        print("4. Details")
        print("5. Exit")
        
        choice = input("Choose an option: ")

        if choice == '1':
            name = input("Enter your name: ")
            service = input("Enter the service required (e.g., Visa, Passport): ")
            date = input("Enter the date (YYYY-MM-DD): ")
            time = input("Enter the time (HH:MM): ")
            system.book_appointment(name, service, date, time)
            appointment = Appointment(name, service, date, time)
            admin.add_appointment_holder(appointment)
        
        elif choice == '2':
            appointment_id = int(input("Enter appointment ID to cancel: "))
            system.cancel_appointment(appointment_id)
        
        elif choice == '3':
            system.view_appointments()
            
        elif choice == '4':
            admin.details()  # Call details from admin instance
        
        elif choice == '5':
            print("Exiting the system.")
            break
        
        else:
            print("Invalid choice, please try again.")

class TestAppointmentServiceSystem(unittest.TestCase):
    def setUp(self):
        self.admin = AppointmentAdmin("localhost", "root", "user", "passport_renewal")
        self.appointment = Appointment('John Doe', 'Passport', '12-12-2022', '12:30')
    
    def test_add_appointment(self):
        self.admin.add_appointment_holder(self.appointment)

    def test_view_details(self):
        self.admin.details()

if __name__ == "__main__":
    main()
import sqlite3
from models import Location, Employee, Animal, Customer

def get_all_locations():
    with sqlite3.connect("./kennel.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            l.id,
            l.name,
            l.address
        FROM Location l
        """)

        locations = []

        dataset = db_cursor.fetchall()
        for row in dataset:
            location = Location(row['id'], row['address'], row['name'])

            locations.append(location.__dict__)

    return locations

def get_single_location(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            l.id,
            l.name,
            l.address
        FROM Location l
        WHERE l.id = ?
        """, ( id, ))
        
        data = db_cursor.fetchone()
        location = Location(data['id'], data['address'], data['name'])
        
        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id
        FROM Employee e
        WHERE e.location_id = ?
        """, ( id, ))

        employees = []
        
        employees_data = db_cursor.fetchall()

        for row in employees_data:
            employee = Employee(row['id'], row['name'], row['location_id'], row['address'])
            employees.append(employee.__dict__)

        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.status,
            a.breed,
            a.customer_id,
            a.location_id,
            c.name customer_name,
            c.address customer_address,
            c.email customer_email
        FROM Animal a
        JOIN Customer c
            ON c.id = a.customer_id
        WHERE a.location_id = ?
        """, ( id, ))

        animals = []
        
        animals_data = db_cursor.fetchall()

        for row in animals_data:
            animal = Animal(row['id'], row['name'], row['breed'],
                            row['status'], row['location_id'],
                            row['customer_id'])
            customer = Customer(row['id'], row['customer_name'], row['customer_address'], row['customer_email'])
            animal.customer = customer.__dict__
            animals.append(animal.__dict__)

        location.employees = employees
        location.animals = animals
        return location.__dict__

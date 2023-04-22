import sqlite3
import json
from models import Customer

def get_all_customers():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            c.id,
            c.name,
            c.address
        FROM customer c
        """)

        # Initialize an empty list to hold all animal representations
        customers = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            customer = Customer(row['id'], row['name'], row['address'])

            customers.append(customer.__dict__)

    return customers

# Function with a single parameter
def get_single_customer(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            c.id,
            c.name,
            c.address
        FROM customer c
        WHERE c.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an customer instance from the current row
        customer = Customer(data['id'], data['name'], data['address'])

        # TODO: you will get an error about the address on customer. Look through the customer model and requests to see if you can solve the issue.
        
        return customer.__dict__
    
def get_customer_by_email(email):

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            c.id,
            c.name,
            c.address,
            c.email,
            c.password
        from Customer c
        WHERE c.email = ?
        """, ( email, ))

        customers = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            customer = Customer(row['id'], row['name'], row['address'], row['email'] , row['password'])
            customers.append(customer.__dict__)

    return customers

# def create_customer(customer):
#     # Get the id value of the last animal in the list
#     max_id = CUSTOMERS[-1]["id"]

#     # Add 1 to whatever that number is
#     new_id = max_id + 1

#     # Add an `id` property to the animal dictionary
#     customer["id"] = new_id

#     # Add the animal dictionary to the list
#     CUSTOMERS.append(customer)

#     # Return the dictionary with `id` property added
#     return customer

# def delete_customer(id):
#     customer_index = -1

#     for index, customer in enumerate(CUSTOMERS):
#         if customer["id"] == id:
#             customer_index = index

#     if customer_index >= 0:
#         CUSTOMERS.pop(customer_index)

# def update_customer(id, new_customer):
#     for index, customer in enumerate(CUSTOMERS):
#         if customer["id"] == id:
#             CUSTOMERS[index] = new_customer
#             break

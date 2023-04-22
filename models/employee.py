class Employee():

    def __init__(self, id, name, location_id, address=""):
        self.id = id
        self.name = name
        self.location_id = location_id
        self.address = address
        self.location = None

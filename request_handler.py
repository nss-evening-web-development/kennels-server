from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs
from views import (get_all_animals, get_single_animal, get_animals_by_location_id,
                   get_animals_by_status, delete_animal, update_animal, create_animal, get_all_locations, get_single_location, get_all_employees, get_single_employee, get_employees_by_location_id, delete_employee, get_all_customers, get_single_customer, get_customer_by_email)

class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """
    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split('/')  # ['', 'animals', 1]
        resource = path_params[1]

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)

        pk = None
        try:
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        """Handles GET requests to the server
        """

        self._set_headers(200)
        response = {}

        parsed = self.parse_url(self.path)

        if '?' not in self.path:
            (resource, id) = parsed

            if resource == "animals":
                if id is not None:
                    response = get_single_animal(id)

                else:
                    response = get_all_animals()

            if resource == "locations":
                if id is not None:
                    response = get_single_location(id)

                else:
                    response = get_all_locations()
            if resource == "employees":
                if id is not None:
                    response = get_single_employee(id)

                else:
                    response = get_all_employees()
            if resource == "customers":
                if id is not None:
                    response = get_single_customer(id)

                else:
                    response = get_all_customers()

        else:  # There is a ? in the path, run the query param functions
            (resource, query) = parsed

            # see if the query dictionary has an email key
            if query.get('email') and resource == 'customers':
                response = get_customer_by_email(query['email'][0])
            # see if the query dictionary has an location_id key
            if query.get('location_id') and resource == 'animals':
                response = get_animals_by_location_id(query['location_id'][0])
            # see if the query dictionary has an location_id key
            if query.get('location_id') and resource == 'employees':
                response = get_employees_by_location_id(
                    query['location_id'][0])
            # see if the query dictionary has an location_id key
            if query.get('status') and resource == 'animals':
                response = get_animals_by_status(query['status'][0])

        # This weird code sends a response back to the client
        # self.wfile.write(f"{response}".encode())
        self.wfile.write(json.dumps(response).encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new animal
        new_entity = None

        if resource == "animals":
            new_entity = create_animal(post_body)

        self.wfile.write(json.dumps(new_entity).encode())

    def do_PUT(self):
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "animals":
            success = update_animal(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)
        
        self.wfile.write("".encode())

    def do_DELETE(self):
        self._set_headers(204)

        (resource, id) = self.parse_url(self.path)

        if resource == "animals":
            delete_animal(id)
        if resource == "employees":
            delete_employee(id)
        
        self.wfile.write("".encode())


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()

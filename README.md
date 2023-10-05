# IP Address Management Tool

## Overview

The IP Address Management Tool is a simple application designed to help ISPs manage and allocate IP addresses to customers, track used and unused IPs, and ensure proper allocation without conflicts.

## Technical Specifications

- **Backend Development**: Django
- **Database**: MySQL (to store IP addresses, their statuses, and associated customer information)
- **API**: Basic API to manage IP addresses
- **Validation**: Proper handling of common networking and IP address validations

## Installation

Follow these steps to set up and run the IP Address Management Tool on your system:

1. **Clone the Repository**:
  
   `git clone https://github.com/yourusername/ip-address-management-tool.git `

2. **Navigate to the Project Directory**:

  cd ip-address-management-tool

4.**Create and activate a virtual environment.** 

  ```
  python3 -m venv venv
  source venv/bin/activate

  ```

4. **Install Dependencies**:
  
   `pip install -r requirements.txt `

5. **Database Setup**:

  Create a MySQL database and configure the database settings in settings.py.
  Apply database migrations:

  ```
  python manage.py makemigrations
  python manage.py migrate
  ```

6. **Run the Application**:

   `python manage.py runserver `

## Endpoints

Allocate IP Address
  Method: POST
  Endpoint: /ip/allocate
  Request Body:
  json
  {
    "customer_name": "John Doe",
    "email": "johndoe@email.com"
  }

  Response:
    Status 201 for success, with allocated IP details.
    Status 400 for bad request.
    Status 500 if no IPs are available.

Release IP Address
  Method: PUT
  Endpoint: /ip/release/{ipAddress}
  Response:
    Status 200 for success.
    Status 404 if IP not found or not allocated.

List Allocated IPs
    Method: GET
    Endpoint: /ip/allocated
    Response:
      Status 200 with a list of allocated IPs and associated customer details.

List Available IPs
    Method: GET
    Endpoint: /ip/available
    Response:
      Status 200 with a list of available IPs.

## Additional Features
  - IP Range Filtering: The application supports filtering IP addresses within a specified range.
  -  Basic Authentication: Endpoints are secured with basic authentication.
  - IP Subnet Calculator Tool: A tool is provided that takes an IP and a subnet mask and returns - the  network address, broadcast address, and usable IP range.

## Live Link

  View the website <a href="https://inspire-an-awwward-clone.herokuapp.com/">here</a>
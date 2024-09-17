# Rental Management System

## Overview

The **Rental Management System** is a web application built using Django, designed to facilitate the management of rental properties. It offers a comprehensive solution for property managers and landlords to handle tenant information, property listings, lease agreements, and maintenance requests. The system provides a user-friendly interface for managing all aspects of property rentals efficiently.

## Features

- **User Authentication**: Secure login and registration for tenants, landlords, and property managers.
- **Property Listings**: Create, update, and manage rental property listings.
- **Tenant Management**: View and manage tenant profiles, leases, and payment history.
- **Lease Agreements**: Generate and manage lease agreements with digital signing capability.
- **Maintenance Requests**: Allow tenants to submit and track maintenance requests.
- **Payment Tracking**: Track rental payments and generate reports.
- **Search and Filter**: Search and filter properties based on various criteria.

## Technologies Used

- **Django**: Web framework for building the application.
- **Python**: Programming language used for backend development.
- **SQLite/PostgreSQL/MySQL**: Database options (depending on configuration).
- **Bootstrap**: Frontend framework for responsive design.
- **Git**: Version control system for managing code.
- **Javascript**
--**CSS** : Styling

## Installation

### Prerequisites

- **Python 3.x**: Ensure Python is installed on your system. You can download it from [python.org](https://www.python.org/).
- **Pip**: Python package installer (comes with Python 3.x).

### Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/steve-ongera/Rentals-Management-System.git
   cd Rentals-Management-System

2. **Create a Virtual Environment**
-python -m venv env

3. **Activate the Virtual Environment**
.\env\Scripts\activate or source env/bin/activate

4. **Install Dependencies**
pip install -r requirements.txt

5. **Apply Migrations**


python manage.py migrate
6. **create a Superuser**

python manage.py createsuperuser
7. **Run the Development Server**

python manage.py runserver

Visit http://127.0.0.1:8000/ in your web browser to access the application.

 ## Usage
Access the Admin Panel: Log in to the Django admin panel at http://127.0.0.1:8000/admin/ using the superuser credentials created during setup.
Manage Properties and Tenants: Use the admin panel to add, update, and manage rental properties and tenant information.
Submit Maintenance Requests: Tenants can submit maintenance requests through the application interface.
Track Payments: View and manage payment records for rental transactions.

## Contributing 
We welcome contributions to the Rental Management System. If you’d like to contribute, please follow these steps:

Fork the Repository: Click the "Fork" button on the GitHub repository page.

**Clone Your Fork:**


git clone https://github.com/your-username/Rentals-Management-System.git
Create a Branch:


git checkout -b feature/your-feature-name
Make Changes and Commit:


git add .
git commit -m "Add feature: your-feature-name"
Push Changes:


git push origin feature/your-feature-name
Open a Pull Request: Go to the original repository on GitHub and open a pull request to merge your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For any questions or support, please contact:
0112284093

Email: gadafisteve0012gmail.com
GitHub: https://github.com/steve-ongera






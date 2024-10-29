Payroll Management System

A simple Django-based payroll management system for tracking employee information, allowances, deductions, and more.

Features

- Employee management: add, delete, edit employee details
- Allowance management: add, edit allowances
- Deduction management: add, edit deductions
- User authentication: login, logout, superuser creation

Requirements

- Python 3.8+
- Django 4.2.16
- mysqlclient 2.1.1
- django-bootstrap5 2.4.2
- XAMPP (Apache, MySQL, PHP)

Installation

1. Install XAMPP and start Apache and MySQL services.
2. Create a database named payroll_db in phpMyAdmin.
3. Import the data.sql file provided in the repository to populate the database.
4. Clone the repository: git clone https://github.com/chisangasage/payroll_system
5. Install dependencies: pip install -r requirements.txt
6. Configure database settings in payroll_project/settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'payroll_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

1. Run migrations: python manage.py migrate
2. Create a superuser: python manage.py createsuperuser
3. Start the server: python manage.py runserver

Usage

- Access the web application at http://localhost:8000
- Login with superuser credentials to access admin features
- Use the navigation menu to explore features

Data Model

The database schema is defined in data.sql. The following tables are used:

- Employees
- Allowances
- Deductions
- Payroll

Troubleshooting

- Ensure XAMPP services are running
- Verify database connection settings
- Check for migration errors
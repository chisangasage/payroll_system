# Payroll Management System (Django + MySQL) - Scaffold

This repository contains a scaffold for a payroll management system using Django.
It includes models for Employee, Department, Allowances, Deductions, PayrollRun and Payslip,
basic CRUD for employees, a dashboard with Chart.js visualization, and admin registration.

## Quick start (development)

1. Create and activate a virtualenv:
   ```
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Configure MySQL:
   - Create a database (e.g. `payroll_db`) and a user with privileges.
   - Either set environment variables:
     ```
     export MYSQL_DB=payroll_db
     export MYSQL_USER=root
     export MYSQL_PASSWORD=yourpassword
     export MYSQL_HOST=127.0.0.1
     export MYSQL_PORT=3306
     ```
   - Or edit `payroll_project/settings.py` DATABASES section.

3. Run migrations and create superuser:
   ```
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```
   

4. Open http://127.0.0.1:8000/ for the dashboard and http://127.0.0.1:8000/admin/ for admin.

## Files included
- `payroll/` - Django app
- `payroll_project/` - Django project settings
- `templates/` - HTML templates (Bootstrap + Chart.js)
- `requirements.txt`, `README.md`

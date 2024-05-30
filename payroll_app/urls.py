from django.urls import path
from . import views

app_name = 'payroll_app'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('register-employee/', views.register_employee, name='register_employee'),
    path('departments_create/', views.create_department, name='create_department'),
    path('benefits/', views.benefits_list, name='benefits_list'),
    path('employees/', views.employees_list, name='employees_list'),
    path('deductions/', views.deductions_list, name='deductions_list'),
    path('employees/<int:employee_id>/edit/', views.edit_employee_view, name='edit_employee'),
    path('search-employee/', views.search_employee, name='search_employee'),
    path('employees/<int:employee_id>/delete/', views.delete_employee_view, name='delete_employee'),
    path('employees/payslip/', views.print_payslip, name='print_payslip'),
    path('employees/payslip/<employee_id>/', views.print_payslip, name='print_payslip'),
]
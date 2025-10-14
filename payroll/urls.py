from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='dashboard'),
    path('employees/', views.employees_list, name='employees_list'),
    path('employees/add/', views.employee_create, name='employee_add'),
    path('employees/<int:pk>/edit/', views.employee_edit, name='employee_edit'),
    path('employees/<int:pk>/delete/', views.employee_delete, name='employee_delete'),
    path('payroll/run/', views.run_payroll, name='run_payroll'),
    path('payroll/<int:pk>/export_pdf/', views.export_payroll_pdf, name='export_payroll_pdf'),
    path('payroll/<int:pk>/payslips/', views.payslip_list, name='payslip_list'),
    path('payslip/<int:pk>/pdf/', views.payslip_pdf, name='payslip_pdf'),
    path('employees/benefits/', views.benefits_index, name='benefits_index'),

    path('allowances/', views.allowances_list, name='allowances_list'),
    path('allowances/add/', views.add_allowance_master, name='add_allowance_master'),
    path('allowances/edit/<int:pk>/', views.edit_allowance_master, name='edit_allowance_master'),
    path('allowances/delete/<int:pk>/', views.delete_allowance_master, name='delete_allowance_master'),
    path('deductions/', views.deductions_list, name='deductions_list'),
    path('deductions/add/', views.add_deduction_master, name='add_deduction_master'),
    path('deductions/edit/<int:pk>/', views.edit_deduction_master, name='edit_deduction_master'),
    path('deductions/delete/<int:pk>/', views.delete_deduction_master, name='delete_deduction_master'),
    path('employees/<int:pk>/benefits/', views.manage_benefits, name='manage_benefits'),

    path('allowance/add/<int:employee_id>/', views.add_allowance, name='add_allowance'),
    path('allowance/<int:pk>/edit/', views.edit_allowance, name='edit_allowance'),
    path('allowance/<int:pk>/delete/', views.delete_allowance, name='delete_allowance'),
    path('deduction/add/<int:employee_id>/', views.add_deduction, name='add_deduction'),
    path('deduction/<int:pk>/edit/', views.edit_deduction, name='edit_deduction'),
    path('deduction/<int:pk>/delete/', views.delete_deduction, name='delete_deduction'),
]

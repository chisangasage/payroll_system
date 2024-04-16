from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('payroll/', views.employee_list, name='employees_list'),
    path('payroll_data/', views.payroll, name='payroll'),
]
from django.shortcuts import render
from django.http import HttpResponse
from .models import Employee, Payroll

def index(request):
    return render(request, 'home.html', {})

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees.html', {'employees':employees})

def payroll(request):
    return HttpResponse('<h1>Payroll</>')
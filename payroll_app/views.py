from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Employee, Payroll

def home(request):
    return render(request, 'home.html', {})

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees.html', {'employees':employees})

def payroll(request):
    return HttpResponse('<h1>Payroll</>')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponse('Logged in successfully')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponse('Logged out successfully')

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm

from .models import Employee, Payroll,User

@login_required(login_url='login')
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to the index page on successful login
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})  # Render the login template with an error message
    return render(request, 'login.html')

def index_view(request):
    return render(request, 'index.html')

def payroll(request):
    return HttpResponse('<h1>Payroll</>')

def logout_view(request):
    logout(request)
    return HttpResponse('Logged out successfully')

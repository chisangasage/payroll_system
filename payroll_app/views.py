from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm

from .models import Employee, Payroll

@login_required(login_url='login')
def index(request):
    return render(request, 'index.html', {})

def payroll(request):
    return HttpResponse('<h1>Payroll</>')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponse('Logged out successfully')

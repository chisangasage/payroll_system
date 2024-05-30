from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('payroll_app:dashboard')  # Redirect to dashboard in payroll_app
        else:
            messages.success(request, 'incorrect username or password try again!!!')
            return redirect('accounts:login')
    else:
        return render(request, 'login.html', {})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('accounts:login')  # Redirect to login page
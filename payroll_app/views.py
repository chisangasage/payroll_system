from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.contrib import messages
from django.conf import settings

from .models import Employee, Benefit, Deduction, Department
from .forms import EmployeeForm, DepartmentForm, BenefitForm, DeductionForm


@login_required(login_url='/login')


def dashboard_view(request):
    current_date = datetime.today()

    # Get customizable next payday from settings (adjust key as needed)
    try:
        next_payday_day = int(settings.PAYDAY_DAY)  # Assuming payday day is an integer in settings
    except (AttributeError, ValueError):
        # Handle potential errors: missing setting or invalid value
        next_payday_day = 15  # Default to 15th if setting is unavailable or invalid

    next_payday = datetime(current_date.year, current_date.month, next_payday_day)
    if current_date.day > next_payday_day:
        next_payday = datetime(current_date.year, current_date.month + 1, next_payday_day)
    days_to_payday = (next_payday - current_date).days

    employee_count = Employee.objects.count()
    total_payroll_amount = 0
    for employee in Employee.objects.all():
        total_payroll_amount += employee.salary
        for benefit in Benefit.objects.all():
            total_payroll_amount += benefit.amount

    context = {
        'days_to_payday': days_to_payday,
        'employee_count': employee_count,
        'total_payroll_amount': total_payroll_amount
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='/login')
def payroll_dashboard(request):
    #payrolls = Payroll.objects.all()
    return render(request, 'payroll_dashboard.html', {})

@login_required(login_url='/login')
def payroll_details(request, payroll_id):
    #payroll = Payroll.objects.get(id=payroll_id)
    #payroll_details = PayrollDetails.objects.filter(payroll=payroll)
    return render(request, 'payroll_details.html', {'payroll_details': payroll_details})

@login_required(login_url='/login')
def create_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_department')
    else:
        form = DepartmentForm()
    return render(request, 'create_department.html', {'form': form})

@login_required(login_url='/login')
def register_employee(request):
    departments = Department.objects.all()
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee Registered Successfully!')  # Use messages
            return redirect('payroll_app:employees_list')
        else:
            print(form.errors)  # Print errors for debugging
    else:
        form = EmployeeForm()

    context = {'form': form, 'departments': departments}
    return render(request, 'register_employee.html', context)

def search_employee(request):
  if request.method == 'POST':
    employee_id = request.POST.get('employee_id')
    try:
      employee = Employee.objects.get(pk=employee_id)
      return redirect('payslip', employee_id=employee.id)
    except Employee.DoesNotExist:
      error_message = 'Employee not found'
      return render(request, 'payslips.html', {'error_message': error_message})
  return render(request, 'payslips.html')

def employees_list(request):
    employees = Employee.objects.all()
    context = {
        'employees': employees
    }
    return render(request, 'employee_list.html', context)

def edit_employee_view(request, employee_id):
    try:
        employee = Employee.objects.get(pk=employee_id)
        if request.method == 'POST':
            form = EmployeeForm(request.POST, instance=employee)
            if form.is_valid():
                form.save()
                messages.success(request, 'Employee details updated successfully!')
                return redirect('payroll_app:employees_list') 
        else:
            form = EmployeeForm(instance=employee)  
    except Employee.DoesNotExist:
        messages.error(request, 'Employee not found!')
        return redirect('payroll_app:employees_list') 

    context = {'form': form}
    return render(request, 'edit_employee.html', context)
def delete_employee_view(request, employee_id):
    try:
        employee = Employee.objects.get(pk=employee_id)
        employee.delete()
        messages.success(request, 'Employee deleted successfully!')
    except Employee.DoesNotExist:
        messages.error(request, 'Employee not found!')
    return redirect('payroll_app:employees_list') 

def benefits_list(request):
    benefits = Benefit.objects.all()
    if request.method == 'POST':
        form = BenefitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payroll_app:benefits_list')
    else:
        form = BenefitForm()
    context = {
        'benefits': benefits,
        'form': form
    }
    return render(request, 'benefits.html', context)


def deductions_list(request):
    deductions = Deduction.objects.all()
    if request.method == 'POST':
        form = DeductionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payroll_app:deductions_list')
    else:
        form = DeductionForm()
    context = {
        'deductions': deductions,
        'form': form
    }
    return render(request, 'deductions.html', context)

def print_payslip(request, employee_id=None):
    if request.method == 'GET':
        employee_id = request.GET.get('employee_id')
    if employee_id:
        employee = get_object_or_404(Employee, employee_id=employee_id)
        benefits = Benefit.objects.filter(employee=employee)
        deductions = Deduction.objects.filter(employee=employee)
        total_benefits = sum(benefit.amount for benefit in benefits)
        total_deductions = sum(deduction.amount for deduction in deductions)
        net_salary = employee.salary + total_benefits - total_deductions
        return render(request, 'payslip.html', {
            'employee': employee,
            'benefits': benefits,
            'deductions': deductions,
            'total_benefits': total_benefits,
            'total_deductions': total_deductions,
            'net_salary': net_salary
        })
    else:
        return render(request, 'search_form.html')
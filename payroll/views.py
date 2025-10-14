from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Employee, PayrollRun, Payslip, Department, EmployeeAllowance, EmployeeDeduction, Allowance, Deduction
from .forms import EmployeeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Sum
import datetime
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from decimal import Decimal, ROUND_HALF_UP

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return render(request, 'payroll/login.html', {'error': 'Invalid credentials'})
    return render(request, 'payroll/login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

@login_required
def home(request):
    from django.db.models import Sum
    import datetime

    total_employees = Employee.objects.count()
    total_departments = Department.objects.count()
    recent_payslips = Payslip.objects.order_by('-created_at')[:5]

    today = datetime.date.today()
    labels, gross_values, deduction_values, net_values = [], [], [], []

    # Show data for last 6 months
    for i in range(5, -1, -1):
        month_date = (today.replace(day=1) - datetime.timedelta(days=30*i)).replace(day=1)
        month_label = month_date.strftime('%b %Y')

        payslips = Payslip.objects.filter(
            payroll__month__year=month_date.year,
            payroll__month__month=month_date.month
        )

        totals = payslips.aggregate(
            gross_sum=Sum('gross_pay'),
            deduction_sum=Sum('total_deductions'),
            net_sum=Sum('net_pay')
        )

        labels.append(month_label)
        gross_values.append(float(totals['gross_sum'] or 0))
        deduction_values.append(float(totals['deduction_sum'] or 0))
        net_values.append(float(totals['net_sum'] or 0))

    context = {
        'total_employees': total_employees,
        'total_departments': total_departments,
        'recent_payslips': recent_payslips,
        'chart_labels': labels,
        'gross_values': gross_values,
        'deduction_values': deduction_values,
        'net_values': net_values,
    }

    return render(request, 'payroll/dashboard.html', context)

@login_required
def employees_list(request):
    employees = Employee.objects.all().prefetch_related('payslip_set')
    for e in employees:
        e.latest_payslip = e.payslip_set.order_by('-created_at').first()
    return render(request, 'payroll/employees_list.html', {'employees': employees})


@login_required
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employees_list')
    else:
        form = EmployeeForm()
    return render(request, 'payroll/employee_form.html', {'form': form, 'title': 'Add Employee'})

@login_required
def employee_edit(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=emp)
        if form.is_valid():
            form.save()
            return redirect('employees_list')
    else:
        form = EmployeeForm(instance=emp)
    return render(request, 'payroll/employee_form.html', {'form': form, 'title': 'Edit Employee'})

@login_required
def employee_delete(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        emp.delete()
        return redirect('employees_list')
    return render(request, 'payroll/employee_confirm_delete.html', {'employee': emp})

@login_required
def run_payroll(request):
    message = None
    created_run = None

    if request.method == 'POST':
        month_str = request.POST.get('month')
        if month_str:
            # Convert month input to a valid date (YYYY-MM)
            month_date = datetime.datetime.strptime(month_str + '-01', '%Y-%m-%d').date()

            # Create the payroll run record
            payroll_run = PayrollRun.objects.create(
                month=month_date,
                processed_by=request.user if request.user.is_authenticated else None
            )

            # Loop through each employee
            employees = Employee.objects.all()

            for emp in employees:
                # --- Calculate Total Allowances ---
                allowances = EmployeeAllowance.objects.filter(employee=emp)
                total_allowances = sum([a.amount for a in allowances]) if allowances else Decimal('0.00')

                # --- Calculate Total Deductions ---
                deductions = EmployeeDeduction.objects.filter(employee=emp)
                total_deductions = sum([d.amount for d in deductions]) if deductions else Decimal('0.00')

                # --- Compute Payroll Values ---
                gross = Decimal(emp.basic_salary) + total_allowances
                net = gross - total_deductions

                # --- Round to 2 decimals ---
                gross = gross.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                total_deductions = total_deductions.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                net = net.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

                # --- Create the Payslip ---
                Payslip.objects.create(
                    payroll=payroll_run,
                    employee=emp,
                    gross_pay=gross,
                    total_deductions=total_deductions,
                    net_pay=net
                )

            message = f"Payroll run created for {month_date:%B %Y} with payslips for {employees.count()} employees."
            return redirect('payslip_list', pk=payroll_run.pk)

    # --- Display recent runs ---
    runs = PayrollRun.objects.order_by('-month')[:20]
    latest_run = PayrollRun.objects.last()

    context = {
        'runs': runs,
        'message': message,
        'latest_run': latest_run
    }

    return render(request, 'payroll/run_payroll.html', context)


@login_required
def payslip_pdf(request, pk):
    payslip = get_object_or_404(Payslip, pk=pk)
    employee = payslip.employee

    # Get employee’s allowances and deductions
    allowances = EmployeeAllowance.objects.filter(employee=employee)
    deductions = EmployeeDeduction.objects.filter(employee=employee)

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Header
    p.setFont('Helvetica-Bold', 16)
    p.drawCentredString(width / 2, height - 50, 'PAYSLIP')
    p.line(50, height - 60, width - 50, height - 60)

    # Employee Details
    p.setFont('Helvetica', 11)
    y = height - 90
    p.drawString(50, y, f"Employee: {employee.first_name} {employee.last_name} ({employee.employee_id})")
    y -= 20
    p.drawString(50, y, f"Department: {employee.department or ''}")
    y -= 20
    p.drawString(50, y, f"Payroll Month: {payslip.payroll.month:%B %Y}")
    y -= 30
    p.setFont('Helvetica-Bold', 12)
    p.drawString(50, y, f"Basic Salary: {employee.basic_salary:.2f}")

    # Allowances Section
    y -= 40
    p.setFont('Helvetica-Bold', 13)
    p.drawString(50, y, "Allowances:")
    y -= 20
    p.setFont('Helvetica', 11)
    if allowances.exists():
        for allow in allowances:
            p.drawString(70, y, f"- {allow.name}: {allow.amount:.2f}")
            y -= 18
    else:
        p.drawString(70, y, "None")
        y -= 18

    # Total Gross Pay
    y -= 5
    p.setFont('Helvetica-Bold', 12)
    p.drawString(50, y, f"Gross Pay: {payslip.gross_pay:.2f}")

    # Deductions Section
    y -= 40
    p.setFont('Helvetica-Bold', 13)
    p.drawString(50, y, "Deductions:")
    y -= 20
    p.setFont('Helvetica', 11)
    if deductions.exists():
        for ded in deductions:
            p.drawString(70, y, f"- {ded.name}: {ded.amount:.2f}")
            y -= 18
    else:
        p.drawString(70, y, "None")
        y -= 18

    # Total Deductions and Net Pay
    y -= 5
    p.setFont('Helvetica-Bold', 12)
    p.drawString(50, y, f"Total Deductions: {payslip.total_deductions:.2f}")
    y -= 25
    p.setFont('Helvetica-Bold', 14)
    p.setFillColor(colors.darkblue)
    p.drawString(50, y, f"Net Pay: {payslip.net_pay:.2f}")
    p.setFillColor(colors.black)

    # Footer
    y -= 40
    p.setFont('Helvetica-Oblique', 9)
    p.drawString(50, y, "This is a system-generated payslip. No signature required.")

    # Finalize
    p.showPage()
    p.save()
    buffer.seek(0)
    return HttpResponse(buffer.getvalue(), content_type='application/pdf')


@login_required
def payslip_list(request, pk):
    """Show list of payslips for a payroll run with links to individual PDF payslips."""
    payroll = get_object_or_404(PayrollRun, pk=pk)
    payslips = payroll.payslips.select_related('employee').all()
    return render(request, 'payroll/payslip_list.html', {'payroll': payroll, 'payslips': payslips})

@login_required
def export_payroll_pdf(request, pk):
    """Export all payslips in a payroll run as a single PDF (one payslip per page)."""
    payroll = get_object_or_404(PayrollRun, pk=pk)
    payslips = payroll.payslips.select_related('employee').all()
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    for payslip in payslips:
        # simple layout per page
        p.setFont('Helvetica-Bold', 14)
        p.drawString(50, height - 50, f'Payslip for: {payslip.employee.first_name} {payslip.employee.last_name}')
        p.setFont('Helvetica', 11)
        y = height - 90
        p.drawString(50, y, f'Employee ID: {payslip.employee.id}')
        y -= 20
        p.drawString(50, y, f'Department: {payslip.employee.department if hasattr(payslip.employee, "department") else ""}')
        y -= 24
        p.drawString(50, y, f'Gross Pay: {payslip.gross_pay}')
        y -= 20
        p.drawString(50, y, f'Total Deductions: {payslip.total_deductions}')
        y -= 24
        p.setFont('Helvetica-Bold', 12)
        p.drawString(50, y, f'Net Pay: {payslip.net_pay}')
        p.showPage()
    p.save()
    buffer.seek(0)
    filename = f'Payroll_{payroll.month:%Y-%m}.pdf'
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

@login_required
def benefits_index(request):
    employees = Employee.objects.all().order_by('last_name','first_name')
    return render(request, 'payroll/benefits_index.html', {'employees': employees})

@login_required
def manage_benefits(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    EmployeeAllowance = globals().get('EmployeeAllowance', None)
    EmployeeDeduction = globals().get('EmployeeDeduction', None)
    # master allowances/deductions
    Allowance = globals().get('Allowance', None)
    Deduction = globals().get('Deduction', None)

    allowances = EmployeeAllowance.objects.filter(employee=emp) if EmployeeAllowance else []
    deductions = EmployeeDeduction.objects.filter(employee=emp) if EmployeeDeduction else []

    common_allowances = Allowance.objects.all() if Allowance else []
    common_deductions = Deduction.objects.all() if Deduction else []

    return render(request, 'payroll/manage_benefits.html', {
        'employee': emp,
        'allowances': allowances,
        'deductions': deductions,
        'common_allowances': common_allowances,
        'common_deductions': common_deductions,
    })

@login_required
def add_allowance(request, employee_id):
    emp = get_object_or_404(Employee, pk=employee_id)
    Allowance = globals().get('Allowance', None)
    EmployeeAllowance = globals().get('EmployeeAllowance', None)

    if request.method == 'POST':
        selected = request.POST.get('selected_allowance')
        if not selected:
            messages.error(request, "Please select an allowance.")
            return redirect('manage_benefits', pk=employee_id)

        if not Allowance or not EmployeeAllowance:
            messages.error(request, "Allowance functionality not available.")
            return redirect('manage_benefits', pk=employee_id)

        allowance = get_object_or_404(Allowance, pk=selected)
        EmployeeAllowance.objects.create(
            employee=emp,
            name=allowance.name,
            amount=allowance.amount
        )
        messages.success(request, f"Added allowance: {allowance.name}")
        return redirect('manage_benefits', pk=employee_id)

    common_allowances = Allowance.objects.all() if Allowance else []
    return render(request, 'payroll/add_allowance.html', {
        'employee': emp,
        'common_allowances': common_allowances
    })

@login_required
def edit_allowance(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    EmployeeAllowance = globals().get('EmployeeAllowance', None)

    if request.method == 'POST':
        name = request.POST.get('name')
        amount = request.POST.get('amount') or 0
        if name:
            EmployeeAllowance.objects.create(employee=emp, name=name, amount=amount)
        return redirect('manage_benefits', pk=pk)

    return render(request, 'payroll/add_allowance.html', {'employee': emp})

@login_required
def delete_allowance(request, pk):
    EmployeeAllowance = globals().get('EmployeeAllowance', None)
    if not EmployeeAllowance:
        return HttpResponse('Allowance model not found', status=404)
    obj = get_object_or_404(EmployeeAllowance, pk=pk)
    emp_pk = obj.employee.pk
    if request.method == 'POST':
        obj.delete()
        return redirect('manage_benefits', pk=emp_pk)
    return render(request, 'payroll/confirm_delete.html', {'obj': obj, 'type': 'allowance'})

@login_required
def manage_deductions(request):
    employees = Employee.objects.all()
    deductions = EmployeeDeduction.objects.select_related('employee')

    if request.method == 'POST':
        emp_id = request.POST.get('employee')
        name = request.POST.get('name')
        amount = request.POST.get('amount')
        if emp_id and name and amount:
            EmployeeDeduction.objects.create(
                employee_id=emp_id, name=name, amount=amount
            )
            return redirect('manage_deductions')

    context = {'deductions': deductions, 'employees': employees}
    return render(request, 'payroll/manage_deductions.html', context)

@login_required
@login_required
def add_deduction(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    deductions = Deduction.objects.all()

    if request.method == 'POST':
        selected_deduction_id = request.POST.get('selected_deduction')
        selected_deduction = get_object_or_404(Deduction, pk=selected_deduction_id)

        # Calculate deduction amount
        if selected_deduction.is_percentage:
            deduction_amount = (selected_deduction.percentage_value / 100) * employee.basic_salary
        else:
            deduction_amount = selected_deduction.amount

        EmployeeDeduction.objects.create(
            employee=employee,
            name=selected_deduction.name,
            amount=deduction_amount
        )

        return redirect('manage_benefits', pk=employee.id)

    return render(request, 'payroll/add_deduction.html', {
        'employee': employee,
        'deductions': deductions
    })

@login_required
def edit_deduction(request, pk):
    deduction = get_object_or_404(EmployeeDeduction, pk=pk)
    employee = deduction.employee

    if request.method == 'POST':
        deduction.name = request.POST.get('name')
        amount = request.POST.get('amount')
        percentage = request.POST.get('percentage')

        if percentage:  # If user entered a percentage
            deduction.amount = (employee.basic_salary * float(percentage)) / 100
        elif amount:
            deduction.amount = amount

        deduction.save()
        return redirect('manage_benefits', pk=employee.pk)

    return render(request, 'payroll/edit_deduction.html', {'deduction': deduction})


@login_required
def delete_deduction(request, pk):
    deduction = get_object_or_404(EmployeeDeduction, pk=pk)
    employee_pk = deduction.employee.pk

    if request.method == 'POST':
        deduction.delete()
        return redirect('manage_benefits', pk=employee_pk)

    return render(request, 'payroll/confirm_delete.html', {
        'obj': deduction,
        'type': 'deduction'
    })

@login_required
def allowances_list(request):
    Allowance = globals().get('Allowance', None)
    allowances = Allowance.objects.all() if Allowance else []
    return render(request, 'payroll/allowances_list.html', {'allowances': allowances})

@login_required
def add_allowance_master(request):
    Allowance = globals().get('Allowance', None)
    if request.method == 'POST':
        name = request.POST.get('name')
        amount = request.POST.get('amount') or 0
        Allowance.objects.create(name=name, amount=amount)
        return redirect('allowances_list')
    return render(request, 'payroll/add_allowance_master.html')

@login_required
def edit_allowance_master(request, pk):
    Allowance = globals().get('Allowance', None)
    if not Allowance:
        return HttpResponse('Allowance model not found', status=404)
    allowance = get_object_or_404(Allowance, pk=pk)
    if request.method == 'POST':
        allowance.name = request.POST.get('name')
        allowance.amount = request.POST.get('amount') or 0
        allowance.save()
        return redirect('allowances_list')
    return render(request, 'payroll/edit_allowance_master.html', {'allowance': allowance})

@login_required
def delete_allowance_master(request, pk):
    Allowance = globals().get('Allowance', None)
    if not Allowance:
        return HttpResponse('Allowance model not found', status=404)
    allowance = get_object_or_404(Allowance, pk=pk)
    if request.method == 'POST':
        allowance.delete()
        return redirect('allowances_list')
    return render(request, 'payroll/confirm_delete.html', {'obj': allowance, 'type': 'allowance'})

@login_required
def deductions_list(request):
    deductions = Deduction.objects.all()
    assignments = EmployeeDeduction.objects.select_related('employee', 'deduction')
    return render(request, 'payroll/deductions_list.html', {
        'deductions': deductions,
        'assignments': assignments
    })

@login_required
def add_deduction_master(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        is_percentage = 'is_percentage' in request.POST
        amount = request.POST.get('amount') or 0
        percentage_value = request.POST.get('percentage_value') or None

        Deduction.objects.create(
            name=name,
            amount=amount,
            is_percentage=is_percentage,
            percentage_value=percentage_value
        )
        return redirect('deductions_list')

    return render(request, 'payroll/add_deduction_master.html')

@login_required
def edit_deduction_master(request, pk):
    deduction = get_object_or_404(Deduction, pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name')
        is_percentage = 'is_percentage' in request.POST
        amount = request.POST.get('amount') or 0
        percentage_value = request.POST.get('percentage_value') or None

        deduction.name = name
        deduction.is_percentage = is_percentage
        deduction.amount = amount
        deduction.percentage_value = percentage_value
        deduction.save()

        return redirect('deductions_list')

    context = {'deduction': deduction}
    return render(request, 'payroll/edit_deduction_master.html', context)


@login_required
def delete_deduction_master(request, pk):
    Deduction = globals().get('Deduction', None)
    if not Deduction:
        return HttpResponse('Deduction model not found', status=404)
    deduction = get_object_or_404(Deduction, pk=pk)
    if request.method == 'POST':
        deduction.delete()
        return redirect('deductions_list')
    return render(request, 'payroll/confirm_delete.html', {'obj': deduction, 'type': 'deduction'})

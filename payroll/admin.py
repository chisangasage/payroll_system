from django.contrib import admin
from .models import Department, Employee, Deduction, Allowance, PayrollRun, Payslip, EmployeeAllowance, EmployeeDeduction
admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(Deduction)
admin.site.register(Allowance)
admin.site.register(EmployeeAllowance)
admin.site.register(EmployeeDeduction)
admin.site.register(PayrollRun)
admin.site.register(Payslip)

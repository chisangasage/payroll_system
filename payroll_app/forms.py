from django import forms
from .models import Department, Employee, Benefit, Deduction


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('name', 'description')

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('employee_id', 'first_name', 'last_name','phone_number', 'department', 'position', 'salary', 'employment_date')
    
    department = forms.ModelChoiceField(queryset=Department.objects.all())


class BenefitForm(forms.ModelForm):
    class Meta:
        model = Benefit
        fields = ('type', 'amount')

class DeductionForm(forms.ModelForm):
    class Meta:
        model = Deduction
        fields = ('type', 'amount')
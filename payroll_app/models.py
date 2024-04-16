from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=255)
    employee_id = models.CharField(max_length=10, unique=True)
    age = models.IntegerField()
    department = models.CharField(max_length=100)

class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    pay_period = models.DateField()
    gross_pay = models.DecimalField(max_digits=10,decimal_places=2)
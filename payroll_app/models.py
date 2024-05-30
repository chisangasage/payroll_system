from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    employee_id = models.CharField(max_length=255, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=12)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    position = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    employment_date = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Benefit(models.Model):
    type = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class Deduction(models.Model):
    type = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)


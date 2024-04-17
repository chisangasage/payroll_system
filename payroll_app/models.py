from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser

class EmailAuthenticator(UserManager):
    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None:
            email = kwargs.get('email')
        if email is None or password is None:
            return None
        try:
            user = self.get(email=email)
        except self.model.DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
    
class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = EmailAuthenticator()


class Employee(models.Model):
    name = models.CharField(max_length=255)
    employee_id = models.CharField(max_length=10, unique=True)
    age = models.IntegerField()
    department = models.CharField(max_length=100)

class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    pay_period = models.DateField()
    gross_pay = models.DecimalField(max_digits=10,decimal_places=2)
# Generated by Django 5.0.4 on 2024-05-10 02:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payroll_app', '0002_payroll_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payroll',
            name='pay_date',
        ),
        migrations.RemoveField(
            model_name='payroll',
            name='pay_period',
        ),
    ]

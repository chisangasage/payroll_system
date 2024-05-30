# Generated by Django 5.0.4 on 2024-05-10 07:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll_app', '0005_employee_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='benefit',
            name='type',
            field=models.CharField(default=0.0, max_length=255),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Deduction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payroll_app.employee')),
            ],
        ),
    ]
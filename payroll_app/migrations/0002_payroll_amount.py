# Generated by Django 5.0.4 on 2024-05-10 02:27

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payroll',
            name='amount',
            field=models.DecimalField(decimal_places=2, default='0.0', max_digits=10),
            preserve_default=False,
        ),
    ]

# Generated by Django 5.0.4 on 2024-04-16 09:35

import payroll_app.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payroll_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', payroll_app.models.EmailAuthenticator()),
            ],
        ),
    ]

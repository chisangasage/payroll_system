# Generated by Django 5.0.4 on 2024-05-10 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll_app', '0004_benefit'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='phone_number',
            field=models.CharField(default=0, max_length=12),
            preserve_default=False,
        ),
    ]

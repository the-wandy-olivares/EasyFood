# Generated by Django 5.1.4 on 2024-12-19 05:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0043_employee_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 3, 0, 0)),
        ),
    ]

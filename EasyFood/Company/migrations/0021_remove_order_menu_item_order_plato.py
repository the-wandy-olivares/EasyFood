# Generated by Django 5.1.4 on 2024-12-11 04:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0020_remove_menuselection_employee_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='menu_item',
        ),
        migrations.AddField(
            model_name='order',
            name='plato',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='plato', to='Company.plato'),
        ),
    ]

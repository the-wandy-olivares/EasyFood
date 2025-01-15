# Generated by Django 5.1.4 on 2024-12-19 14:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0046_menuchoices_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories_company', to='Company.company'),
        ),
        migrations.AddField(
            model_name='category',
            name='is_company',
            field=models.BooleanField(default=False),
        ),
    ]

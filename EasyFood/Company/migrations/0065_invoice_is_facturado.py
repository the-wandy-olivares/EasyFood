# Generated by Django 5.1.4 on 2025-02-06 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0064_alter_company_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='is_facturado',
            field=models.BooleanField(default=False),
        ),
    ]

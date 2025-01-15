# Generated by Django 5.1.4 on 2024-12-16 04:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0038_plato_img1_plato_img2'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories_service', to='Company.service'),
        ),
    ]

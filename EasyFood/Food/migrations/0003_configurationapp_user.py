# Generated by Django 5.1.4 on 2024-12-13 18:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Food', '0002_rename_configuration_configurationapp'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='configurationapp',
            name='user',
            field=models.OneToOneField(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='configuration_app', to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
    ]

# Generated by Django 5.1.4 on 2024-12-19 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0045_menuchoices_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuchoices',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]

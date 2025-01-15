# Generated by Django 5.1.4 on 2024-12-13 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='Restaurante')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='media/logo/')),
                ('address', models.CharField(blank=True, max_length=255, verbose_name='Dirección')),
                ('phone', models.CharField(blank=True, max_length=15, verbose_name='Teléfono')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Correo Electrónico')),
                ('ui_theme', models.CharField(blank=True, max_length=50, verbose_name='Tema UI')),
                ('animations', models.BooleanField(blank=True, default=True, verbose_name='Animaciones')),
            ],
            options={
                'verbose_name': 'Configuración',
                'verbose_name_plural': 'Configuraciones',
            },
        ),
    ]

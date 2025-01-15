from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ConfigurationApp(models.Model):
      user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='configuration_app', verbose_name="Usuario", blank=True, default=1)
      name = models.CharField(max_length=255, verbose_name="Restaurante", blank=True)
      logo = models.ImageField(upload_to='media/logo/', null=True, blank=True)
      address = models.CharField(max_length=255, verbose_name="Dirección", blank=True)
      phone = models.CharField(max_length=15, verbose_name="Teléfono", blank=True)
      email = models.EmailField(verbose_name="Correo Electrónico", blank=True)

      # Configuracion de ui
      ui_theme = models.CharField(max_length=50, verbose_name="Tema UI", blank=True)
      animations = models.BooleanField(default=True, verbose_name="Animaciones", blank=True)

      class Meta:
            verbose_name = "Configuración"
            verbose_name_plural = "Configuraciones"


      def __str__(self):
            return self.name
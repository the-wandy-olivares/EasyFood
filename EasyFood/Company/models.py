from django.db import models

class Company(models.Model):
      SERVICE_OPTIONS = [
            ('desayuno', 'Desayuno'),
            ('comida', 'Comida'),
            ('cena', 'Cena'),
      ]

      name = models.CharField(max_length=255, verbose_name="Nombre", blank=True)
      img = models.ImageField(upload_to='media/company/', null=True, blank=True)
      tax_id = models.CharField(max_length=50, unique=True, verbose_name="Tax ID", blank=True)
      address = models.TextField(verbose_name="Address", blank=True)
      phone = models.CharField(max_length=15, verbose_name="Phone", blank=True)
      email = models.EmailField(verbose_name="Email Address", blank=True)
      representative = models.CharField(max_length=255, verbose_name="Main Representative", blank=True)
      services = models.ManyToManyField('Service', related_name='companies', verbose_name="Contracted Services", blank=True)
      is_active = models.BooleanField(default=True)

      class Meta:
            verbose_name = "Client Company"
            verbose_name_plural = "Client Companies"

      def __str__(self):
            return self.name


class Service(models.Model):
      name = models.CharField(max_length=50, choices=Company.SERVICE_OPTIONS, unique=True, blank=True)

      class Meta:
            verbose_name = "Service"
            verbose_name_plural = "Services"

      def __str__(self):
            return self.get_name_display()
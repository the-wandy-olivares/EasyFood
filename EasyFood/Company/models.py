from django.db import models
from django.contrib.auth.models import User

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
      representative = models.CharField(max_length=255, verbose_name="Principal reprentante", blank=True)
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




class Employee(models.Model):
      ROLE_OPTIONS = [
                  ('ejecutivo', 'Ejecutivo'),
                  ('estandar', 'Estandar'),
      ]
      GENERO = [
                  ('masculino', 'Masculino'),
                  ('femenino', 'Femenino'),
      ]

      user = models.OneToOneField(
            User, 
            on_delete=models.CASCADE, 
            related_name='employee_profile',
            verbose_name="User", blank=True
      )
      
      company = models.ForeignKey( 'Company', on_delete=models.CASCADE, 
      related_name='employee', verbose_name='Company', blank=True)
      username = models.CharField(default='employee', max_length=80)
      password = models.CharField(max_length=100)
      first_name = models.CharField(max_length=255, verbose_name="Nombre", blank=True)
      last_name = models.CharField(max_length=255, verbose_name="Apellidos", blank=True)
      email = models.EmailField(unique=True, verbose_name="Correo electronico", blank=True)
      phone = models.CharField(max_length=15, verbose_name="Numero de telefono", blank=True, null=True)
      role = models.CharField(max_length=10, choices=ROLE_OPTIONS, verbose_name="Role", blank=True)
      genero = models.CharField(max_length=10, choices=GENERO, verbose_name="Genero", blank=True)
      is_active = models.BooleanField(default=True, verbose_name="Estado activo", blank=True)

      class Meta:
            verbose_name = "Employee"
            verbose_name_plural = "Employees"

      def __str__(self):
            return f"{self.first_name} {self.last_name} - {self.company.name}"



class Menu(models.Model):
      DAY_CHOICES = [
            ('monday', 'Lunes'),
            ('tuesday', 'Martes'),
            ('wednesday', 'Miércoles'),
            ('thursday', 'Jueves'),
            ('friday', 'Viernes'),
            ('saturday', 'Sábado'),
            ('sunday', 'Domingo'),
      ]
      name = models.CharField(max_length=255, verbose_name="Plato")
      day = models.CharField(max_length=10, choices=DAY_CHOICES, verbose_name="Día")
      time = models.CharField(max_length=20, verbose_name="Horario (ej. desayuno, almuerzo, cena)")

      class Meta:
            verbose_name = "Menú"
            verbose_name_plural = "Menús"

      def __str__(self):
            return f"{self.name} ({self.day} - {self.time})"


class Order(models.Model):
      employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="orders", blank=True)
      menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE, blank=True, related_name='menu_item')  # Relacionado con el plato seleccionado
      date = models.DateTimeField(auto_now_add=True)  # Fecha y hora del pedido
      status = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('completado', 'Completado')], default='pendiente')


      class Meta:
            verbose_name = "Pedido"
            verbose_name_plural = "Pedidos"

      def __str__(self):
            return f"{self.employee} - {self.menu_item} - {self.date}"


# Consultar montos facturados y pagos pendientes
class Invoice(models.Model):
      company = models.ForeignKey(Company, related_name='invoices', on_delete=models.CASCADE)
      amount = models.DecimalField(max_digits=10, decimal_places=2)
      date_issued = models.DateField()
      due_date = models.DateField()
      paid = models.BooleanField(default=False)
      payment_date = models.DateField(null=True, blank=True)

      def __str__(self):
            return f"Invoice {self.id} - {self.company.name}"


class Payment(models.Model):
      invoice = models.ForeignKey(Invoice, related_name='payments', on_delete=models.CASCADE)
      amount = models.DecimalField(max_digits=10, decimal_places=2)
      payment_date = models.DateField()

      def __str__(self):
            return f"Payment for Invoice {self.invoice.id}"